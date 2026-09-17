from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from resource_utils import resource_path
import webbrowser
import threading
import os
import database
from calculator import calculate_allowances
from tafqeet import tafqeet
from pdf_generator import generate_pdf_report
from excel_generator import generate_excel_report

template_dir = resource_path('templates')
static_dir = resource_path('static') # optional if used later
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
database.init_db()

@app.route('/')
def dashboard():
    total_missions, total_spent = database.get_stats()
    return render_template('dashboard.html', m_count=total_missions, m_spent=total_spent)


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        data = {
            'republic_title': request.form.get('republic_title'),
            'ministry_name': request.form.get('ministry_name'),
            'state_name': request.form.get('state_name'),
            'institution_name': request.form.get('institution_name'),
            'default_chapter': request.form.get('default_chapter'),
            'default_article': request.form.get('default_article')
        }
        database.update_settings(data)
        return redirect(url_for('settings'))

    curr_settings = database.get_settings()
    return render_template('settings.html', settings=curr_settings)

@app.route('/employees', methods=['GET', 'POST'])
def employees():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            data = {
                'full_name': request.form.get('name'),
                'rank': request.form.get('rank'),
                'job_title': request.form.get('job'),
                'index_number': request.form.get('index'),
                'category': request.form.get('category'),
                'workplace': request.form.get('workplace'),
                'bank_type': request.form.get('bank_type'),
                'bank_account': request.form.get('bank_account')
            }
            if data['full_name']:
                database.add_employee(data)
        elif action == 'edit':
            emp_id = request.form.get('emp_id')
            data = {
                'full_name': request.form.get('name'),
                'rank': request.form.get('rank'),
                'job_title': request.form.get('job'),
                'index_number': request.form.get('index'),
                'category': request.form.get('category'),
                'workplace': request.form.get('workplace'),
                'bank_type': request.form.get('bank_type'),
                'bank_account': request.form.get('bank_account')
            }
            if emp_id and data['full_name']:
                database.update_employee(int(emp_id), data)
        elif action == 'delete':
            emp_id = request.form.get('emp_id')
            if emp_id:
                database.delete_employee(int(emp_id))
        return redirect(url_for('employees'))

    emps = database.get_all_employees()
    return render_template('employees.html', employees=emps)

@app.route('/missions', methods=['GET', 'POST'])
def missions():
    emps = database.get_all_employees()
    selected_emp_id = request.args.get('emp_id')
    if not selected_emp_id and emps:
        selected_emp_id = str(emps[0][0])

    if request.method == 'POST':
        action = request.form.get('action')
        selected_emp_id = request.form.get('emp_id')

        if action == 'delete':
            mis_id = request.form.get('mission_id')
            if mis_id:
                database.delete_mission(int(mis_id))
        elif action == 'add':
            dep = request.form.get('departure_datetime')
            ret = request.form.get('return_datetime')
            reg = request.form.get('region')

            is_training = (request.form.get('mission_type') == 'تكوين')
            m_count, n_count, gross, tot = calculate_allowances(dep, ret, reg, is_training=is_training)
            t_txt = tafqeet(tot)

            data = {
                'budget_chapter': request.form.get('budget_chapter'),
                'budget_article': request.form.get('budget_article'),
                'report_month_year': request.form.get('report_month_year'),
                'order_number': request.form.get('order_number'),
                'order_date': request.form.get('order_date'),
                'purpose': request.form.get('purpose'),
                'itinerary': request.form.get('itinerary'),
                'transport_mode': request.form.get('transport_mode'),
                'departure_datetime': dep,
                'return_datetime': ret,
                'region': reg,
                'meals_count': m_count,
                'nights_count': n_count,
                'total_amount': tot,
                'amount_text': t_txt,
                'mission_type': request.form.get('mission_type', 'عادية')
            }
            if selected_emp_id:
                database.add_mission(int(selected_emp_id), data)


        elif action == 'edit':
            mis_id = request.form.get('mission_id')
            dep = request.form.get('departure_datetime')
            ret = request.form.get('return_datetime')
            reg = request.form.get('region')

            is_training = (request.form.get('mission_type') == 'تكوين')
            m_count, n_count, gross, tot = calculate_allowances(dep, ret, reg, is_training=is_training)
            t_txt = tafqeet(tot)

            data = {
                'budget_chapter': request.form.get('budget_chapter'),
                'budget_article': request.form.get('budget_article'),
                'report_month_year': request.form.get('report_month_year'),
                'order_number': request.form.get('order_number'),
                'order_date': request.form.get('order_date'),
                'purpose': request.form.get('purpose'),
                'itinerary': request.form.get('itinerary'),
                'transport_mode': request.form.get('transport_mode'),
                'departure_datetime': dep,
                'return_datetime': ret,
                'region': reg,
                'meals_count': m_count,
                'nights_count': n_count,
                'total_amount': tot,
                'amount_text': t_txt,
                'mission_type': request.form.get('mission_type', 'عادية')
            }
            if mis_id:
                database.update_mission(int(mis_id), data)

        return redirect(url_for('missions', emp_id=selected_emp_id))

    missions_list = database.get_missions_for_employee(selected_emp_id) if selected_emp_id else []
    return render_template('missions.html', employees=emps, missions=missions_list, selected_emp_id=selected_emp_id)

@app.route('/calc_preview', methods=['POST'])
def calc_preview():
    data = request.json
    is_training = (data.get('mission_type') == 'تكوين')
    m_count, n_count, gross, net = calculate_allowances(
        data.get('dep'), data.get('ret'), data.get('reg'), is_training=is_training
    )
    t_txt = tafqeet(net)
    return jsonify({
        'meals': m_count,
        'nights': n_count,
        'gross': gross,
        'total': net,
        'text': t_txt,
        'is_training': is_training
    })

@app.route('/export/<type>/<emp_id>')
def export_report(type, emp_id):
    emp = database.get_employee(int(emp_id))
    missions_list = database.get_missions_for_employee(int(emp_id))

    if not emp or not missions_list:
        return "لا توجد بيانات أو مهمات لهذا الموظف لتصديرها", 404

    # Recalculate Grand Total for Tafqeet
    grand_total = sum(m[15] for m in missions_list)
    tafqeet_text = tafqeet(grand_total)

    if type == "pdf":
        path = f"report_employee_{emp_id}.pdf"
        generate_pdf_report(emp, missions_list, path, tafqeet_text, database.get_settings())
        return send_file(path, as_attachment=True)
    elif type == "excel":
        path = f"report_employee_{emp_id}.xlsx"
        generate_excel_report(emp, missions_list, path, tafqeet_text, database.get_settings())
        return send_file(path, as_attachment=True)

    return "Invalid type", 400


@app.route('/export_all/excel')
def export_all_excel():
    all_employees = database.get_all_employees()
    employees_data = []

    for emp in all_employees:
        emp_id = emp[0]
        missions = database.get_missions_for_employee(emp_id)
        if missions:
            employees_data.append((emp, missions))

    if not employees_data:
        return "لا توجد أي مهام مسجلة للموظفين لتصديرها.", 404

    output_filename = "كشف_المهام_الإجمالي_لكافة_الموظفين.xlsx"
    from excel_generator import generate_consolidated_excel_report
    generate_consolidated_excel_report(employees_data, output_filename, settings=database.get_settings())

    return send_file(output_filename, as_attachment=True)
