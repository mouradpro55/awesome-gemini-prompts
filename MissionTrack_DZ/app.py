from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from resource_utils import resource_path
import subprocess
import time
import os

def get_safe_output_path(filepath):
    if os.path.exists(filepath):
        try:
            with open(filepath, 'a'):
                pass
        except PermissionError:
            timestamp = time.strftime("%H%M%S")
            base, ext = os.path.splitext(filepath)
            return f"{base}_{timestamp}{ext}"
    return filepath
import webbrowser
import threading
import os
import time
import database
from calculator import calculate_allowances
from tafqeet import tafqeet
from pdf_generator import generate_pdf_report
from pdf_generator import generate_pdf_report
from excel_generator import generate_excel_report, generate_consolidated_excel_report
from engagement_generator import generate_engagement_doc

def get_user_downloads_dir():
    home = os.path.expanduser("~")
    downloads = os.path.join(home, "Downloads")
    if not os.path.exists(downloads):
        downloads = os.path.join(home, "Documents")
    if not os.path.exists(downloads):
        os.makedirs(downloads, exist_ok=True)
    return downloads

def open_file_externally(filepath):
    try:
        if os.name == 'nt':
            os.startfile(filepath)
        else:
            subprocess.Popen(['xdg-open', filepath])
    except Exception as e:
        print(f"Error opening file: {e}")


template_dir = resource_path('templates')
static_dir = resource_path('static') # optional if used later
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
database.init_db()

@app.route('/')
def dashboard():
    total_missions, total_spent = database.get_stats()
    return render_template('dashboard.html', m_count=total_missions, m_spent=total_spent)



@app.route('/export_engagement/<emp_id>')
def export_engagement(emp_id):
    try:
        emp = database.get_employee(int(emp_id))
        missions_list = database.get_missions_for_employee(int(emp_id))
        if not emp or not missions_list:
            return "لا توجد مهمات مسجلة لهذا الموظف لإنشاء بطاقة الالتزام.", 404

        # حساب المبلغ المقترح للكشف الحالي
        proposed_amt = sum(m[15] for m in missions_list)

        summary = database.get_budget_summary()

        # Fetch params from request if available, otherwise use defaults
        req_card_num = request.args.get('card_number', f"0{emp_id}")
        req_card_date = request.args.get('card_date', missions_list[-1][6] if missions_list[-1][6] else "06-04-2026")

        req_prior_str = request.args.get('prior_commitments')
        if req_prior_str is not None and req_prior_str.strip() != "":
            prior_commitments = float(req_prior_str)
        else:
            prior_commitments = max(0.0, summary['total_consumed'] - proposed_amt)

        req_alloc_str = request.args.get('allocated_budget')
        if req_alloc_str is not None and req_alloc_str.strip() != "":
            allocated_ae = float(req_alloc_str)
        else:
            allocated_ae = summary['allocated_budget']

        budget_info = database.get_budget_credit_info()
        save_dir = get_user_downloads_dir()

        emp_clean = "".join(c for c in emp[1] if c.isalnum() or c in (' ', '_', '-')).strip().replace(" ", "_")
        filename = f"بطاقة_التزام_{emp_clean}.docx".replace(" ", "_")
        out_path = os.path.join(save_dir, filename)
        out_path = get_safe_output_path(out_path)

        generate_engagement_doc(
            output_path=out_path,
            employee=emp,
            proposed_amount=proposed_amt,
            prior_commitments=prior_commitments,
            budget_info=budget_info,
            commitment_num=req_card_num,
            commitment_date=req_card_date,
            allocated_ae=allocated_ae
        )
        open_file_externally(out_path)
        return redirect(url_for('missions', emp_id=emp_id))
    except Exception as e:
        print(f"Export engagement error: {e}")
        return f"خطأ أثناء توليد بطاقة الالتزام: {e}", 500

@app.route('/budget', methods=['GET', 'POST'])
def budget():
    if request.method == 'POST':
        data = {
            'program_code': request.form.get('program_code'),
            'program_name': request.form.get('program_name'),
            'subprogram_code': request.form.get('subprogram_code'),
            'subprogram_name': request.form.get('subprogram_name'),
            'activity_code': request.form.get('activity_code'),
            'activity_name': request.form.get('activity_name'),
            'order_officer_code': request.form.get('order_officer_code'),
            'class_code': request.form.get('class_code'),
            'class_name': request.form.get('class_name'),
            'allocated_budget': request.form.get('allocated_budget')
        }
        database.update_budget_credit_info(data)
        return redirect(url_for('budget'))

    summary = database.get_budget_summary()
    info = database.get_budget_credit_info()
    return render_template('budget.html', summary=summary, info=info)

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
    summary = database.get_budget_summary()
    return render_template('missions.html', employees=emps, missions=missions_list, selected_emp_id=selected_emp_id, summary=summary)

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
    try:
        emp = database.get_employee(int(emp_id))
        missions_list = database.get_missions_for_employee(int(emp_id))

        if not emp or not missions_list:
            return "لا توجد بيانات أو مهمات لهذا الموظف لتصديرها", 404

        grand_total = sum(m[15] for m in missions_list)
        tafqeet_text = tafqeet(grand_total)

        save_dir = get_user_downloads_dir()
        emp_clean_name = "".join(c for c in emp[1] if c.isalnum() or c in (' ', '_', '-')).strip().replace(" ", "_")

        if type == "pdf":
            filename = f"كشف_مهمات_{emp_clean_name}.pdf"
            output_path = os.path.join(save_dir, filename)
            output_path = get_safe_output_path(output_path)
            generate_pdf_report(emp, missions_list, output_path, tafqeet_text, database.get_settings())
            open_file_externally(output_path)
            return redirect(url_for('missions', emp_id=emp_id))

        elif type == "excel":
            filename = f"كشف_مهمات_{emp_clean_name}.xlsx"
            output_path = os.path.join(save_dir, filename)
            output_path = get_safe_output_path(output_path)
            generate_excel_report(emp, missions_list, output_path, tafqeet_text, database.get_settings())
            open_file_externally(output_path)
            return redirect(url_for('missions', emp_id=emp_id))

        return "Invalid type", 400
    except Exception as e:
        print(f"Export error: {e}")
        return f"حدث خطأ أثناء تصدير الكشف: {e}", 500


@app.route('/export_all/excel')
def export_all_excel():
    try:
        all_employees = database.get_all_employees()
        employees_data = []

        for emp in all_employees:
            emp_id = emp[0]
            missions = database.get_missions_for_employee(emp_id)
            if missions:
                employees_data.append((emp, missions))

        if not employees_data:
            return "لا توجد أي مهام مسجلة للموظفين لتصديرها.", 404

        save_dir = get_user_downloads_dir()
        output_filename = os.path.join(save_dir, "كشف_المهام_الإجمالي_لكافة_الموظفين.xlsx")
        output_filename = get_safe_output_path(output_filename)

        from excel_generator import generate_consolidated_excel_report
        generate_consolidated_excel_report(employees_data, output_filename, settings=database.get_settings())
        open_file_externally(output_filename)

        return redirect(url_for('missions'))
    except Exception as e:
        print(f"Export all error: {e}")
        return f"حدث خطأ أثناء تصدير الملف الشامل: {e}", 500
