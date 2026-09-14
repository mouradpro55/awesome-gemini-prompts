import customtkinter as ctk
from tkinter import messagebox, filedialog
from bidi.algorithm import get_display
import arabic_reshaper
import database
from calculator import calculate_allowances
from tafqeet import tafqeet
from pdf_generator import generate_pdf_report
from excel_generator import generate_excel_report
import os

def render_ar(text):
    if not text: return ""
    return get_display(arabic_reshaper.reshape(str(text)))

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class MissionTrackApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(render_ar("MissionTrack DZ - نافذتي للتنقل"))
        self.geometry("900x650")

        database.init_db()

        # Grid Layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- Sidebar ---
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=2, sticky="nsew") # Right side for RTL
        self.sidebar.grid_rowconfigure(5, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar, text=render_ar("MissionTrack DZ"), font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btn_dash = ctk.CTkButton(self.sidebar, text=render_ar("لوحة القيادة"), command=lambda: self.show_frame("dash"))
        self.btn_dash.grid(row=1, column=0, padx=20, pady=10)

        self.btn_emp = ctk.CTkButton(self.sidebar, text=render_ar("إدارة الموظفين"), command=lambda: self.show_frame("emp"))
        self.btn_emp.grid(row=2, column=0, padx=20, pady=10)

        self.btn_mis = ctk.CTkButton(self.sidebar, text=render_ar("إدارة الكشوفات"), command=lambda: self.show_frame("mis"))
        self.btn_mis.grid(row=3, column=0, padx=20, pady=10)

        self.btn_about = ctk.CTkButton(self.sidebar, text=render_ar("حول البرنامج"), command=lambda: self.show_frame("about"))
        self.btn_about.grid(row=4, column=0, padx=20, pady=10)

        self.theme_menu = ctk.CTkOptionMenu(self.sidebar, values=[render_ar("فاتح"), render_ar("داكن")], command=self.change_theme)
        self.theme_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")
        self.theme_menu.set(render_ar("داكن") if ctk.get_appearance_mode() == "Dark" else render_ar("فاتح"))

        # --- Main Content Area ---
        self.frames = {}

        # 1. Dashboard
        self.frames["dash"] = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.frames["dash"].grid_columnconfigure(0, weight=1)

        self.dash_title = ctk.CTkLabel(self.frames["dash"], text=render_ar("مرحباً بك في نظام تسيير المهمات"), font=ctk.CTkFont(size=24, weight="bold"))
        self.dash_title.grid(row=0, column=0, pady=30)

        self.stats_label = ctk.CTkLabel(self.frames["dash"], text="", font=ctk.CTkFont(size=18))
        self.stats_label.grid(row=1, column=0, pady=20)

        # 2. Employees
        self.frames["emp"] = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.setup_emp_frame()

        # 3. Missions
        self.frames["mis"] = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.setup_mis_frame()

        # 4. About
        self.frames["about"] = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.frames["about"].grid_columnconfigure(0, weight=1)
        about_text = (
            "برنامج نافذتي للتنقل - MissionTrack DZ\n\n"
            "النسخة: 1.0.0\n"
            "تصميم وتطوير: السيد مصباح مراد\n\n"
            "مخصص لقطاع المواصلات السلكية واللاسلكية\n"
            "لأتمتة عملية إعداد ومراجعة وحساب كشوف مصاريف التنقل"
        )
        self.about_lbl = ctk.CTkLabel(self.frames["about"], text=render_ar(about_text), font=ctk.CTkFont(size=16), justify="center")
        self.about_lbl.grid(row=0, column=0, pady=100)

        self.show_frame("dash")

    def change_theme(self, choice):
        if render_ar("داكن") in choice:
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")

    def show_frame(self, name):
        for frame in self.frames.values():
            frame.grid_forget()
        self.frames[name].grid(row=0, column=1, sticky="nsew")

        if name == "dash":
            t_mis, t_spent = database.get_stats()
            stats_text = f"إجمالي المهمات المسجلة: {t_mis}\nإجمالي المصروفات: {t_spent} دج"
            self.stats_label.configure(text=render_ar(stats_text))
        elif name == "mis":
            self.refresh_emp_dropdown()
            self.refresh_mis_dropdown()

    def setup_emp_frame(self):
        f = self.frames["emp"]
        f.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(f, text=render_ar("إضافة موظف جديد")).grid(row=0, column=0, columnspan=2, pady=10)

        self.e_name = ctk.CTkEntry(f, placeholder_text=render_ar("الاسم واللقب"))
        self.e_name.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.e_rank = ctk.CTkEntry(f, placeholder_text=render_ar("الرتبة"))
        self.e_rank.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.e_job = ctk.CTkEntry(f, placeholder_text=render_ar("الوظيفة"))
        self.e_job.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.e_idx = ctk.CTkEntry(f, placeholder_text=render_ar("الرقم الاستدلالي"))
        self.e_idx.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self.e_cat = ctk.CTkEntry(f, placeholder_text=render_ar("الصنف"))
        self.e_cat.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        self.e_work = ctk.CTkEntry(f, placeholder_text=render_ar("المقر الإداري"))
        self.e_work.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        self.e_btype = ctk.CTkOptionMenu(f, values=["CCP", "BNA", "BEA"])
        self.e_btype.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        self.e_bacc = ctk.CTkEntry(f, placeholder_text=render_ar("رقم الحساب"))
        self.e_bacc.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

        ctk.CTkButton(f, text=render_ar("حفظ الموظف"), command=self.save_emp).grid(row=5, column=0, columnspan=2, pady=15)

    def save_emp(self):
        data = {
            'full_name': self.e_name.get(),
            'rank': self.e_rank.get(),
            'job_title': self.e_job.get(),
            'index_number': self.e_idx.get(),
            'category': self.e_cat.get(),
            'workplace': self.e_work.get(),
            'bank_type': self.e_btype.get(),
            'bank_account': self.e_bacc.get()
        }
        if not data['full_name']:
            messagebox.showwarning("تنبيه", "الاسم واللقب مطلوب")
            return
        database.add_employee(data)
        messagebox.showinfo("نجاح", "تم الحفظ بنجاح")
        self.e_name.delete(0, 'end')

    def setup_mis_frame(self):
        f = self.frames["mis"]
        f.grid_columnconfigure((0, 1), weight=1)

        self.m_emp_combo = ctk.CTkOptionMenu(f, values=[])
        self.m_emp_combo.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        ctk.CTkLabel(f, text=render_ar("اختر الموظف:")).grid(row=0, column=0, sticky="e", padx=10)

        # Inputs
        self.m_order = ctk.CTkEntry(f, placeholder_text=render_ar("رقم الأمر بمهمة"))
        self.m_order.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.m_date = ctk.CTkEntry(f, placeholder_text=render_ar("تاريخ الأمر"))
        self.m_date.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.m_purp = ctk.CTkEntry(f, placeholder_text=render_ar("سبب التنقل"))
        self.m_purp.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.m_itin = ctk.CTkEntry(f, placeholder_text=render_ar("المسار (من - إلى)"))
        self.m_itin.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self.m_dep = ctk.CTkEntry(f, placeholder_text=render_ar("الذهاب (DD-MM-YYYY HH:MM)"))
        self.m_dep.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        self.m_ret = ctk.CTkEntry(f, placeholder_text=render_ar("الإياب (DD-MM-YYYY HH:MM)"))
        self.m_ret.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        self.m_trans = ctk.CTkEntry(f, placeholder_text=render_ar("وسيلة النقل (مثال: سيارة إدارية)"))
        self.m_trans.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
        self.m_reg = ctk.CTkOptionMenu(f, values=[render_ar("شمال"), render_ar("جنوب")])
        self.m_reg.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

        # Additional Budget Info
        self.m_chap = ctk.CTkEntry(f, placeholder_text=render_ar("الباب المالي"))
        self.m_chap.grid(row=5, column=1, padx=10, pady=5, sticky="ew")
        self.m_art = ctk.CTkEntry(f, placeholder_text=render_ar("المادة"))
        self.m_art.grid(row=5, column=0, padx=10, pady=5, sticky="ew")

        self.m_month = ctk.CTkEntry(f, placeholder_text=render_ar("شهر وسنة الكشف (مثال: ماي 2026)"))
        self.m_month.grid(row=6, column=1, padx=10, pady=5, sticky="ew")

        # Calc Button
        ctk.CTkButton(f, text=render_ar("حساب آلي"), command=self.calc_mission).grid(row=7, column=1, pady=10)

        # Results
        self.m_meals = ctk.CTkEntry(f, placeholder_text=render_ar("الوجبات"))
        self.m_meals.grid(row=8, column=1, padx=10, pady=5)
        self.m_nights = ctk.CTkEntry(f, placeholder_text=render_ar("الليالي"))
        self.m_nights.grid(row=8, column=0, padx=10, pady=5)

        ctk.CTkButton(f, text=render_ar("حفظ الكشف"), command=self.save_mission).grid(row=9, column=0, columnspan=2, pady=10)

        # Export Section
        self.export_combo = ctk.CTkOptionMenu(f, values=[])
        self.export_combo.grid(row=10, column=1, padx=10, pady=20, sticky="ew")
        ctk.CTkButton(f, text=render_ar("تصدير PDF"), command=self.export_pdf).grid(row=10, column=0, padx=10, pady=20, sticky="w")
        ctk.CTkButton(f, text=render_ar("تصدير Excel"), command=self.export_excel).grid(row=10, column=0, padx=10, pady=20, sticky="e")

    def refresh_emp_dropdown(self):
        emps = database.get_all_employees()
        self.emp_map = {render_ar(f"{e[1]} - {e[4]}"): e[0] for e in emps}
        vals = list(self.emp_map.keys()) if self.emp_map else [render_ar("لا يوجد موظفين")]
        self.m_emp_combo.configure(values=vals)
        if vals: self.m_emp_combo.set(vals[0])

    def refresh_mis_dropdown(self):
        try:
            emp_str = self.m_emp_combo.get()
            emp_id = self.emp_map.get(emp_str)
            if emp_id:
                missions = database.get_missions_for_employee(emp_id)
                self.mis_map = {render_ar(f"مهمة: {m[4]} - {m[6]}"): m[0] for m in missions}
                vals = list(self.mis_map.keys()) if self.mis_map else [render_ar("لا توجد مهمات")]
                self.export_combo.configure(values=vals)
                if vals: self.export_combo.set(vals[0])
        except:
            pass

    def calc_mission(self):
        dep = self.m_dep.get()
        ret = self.m_ret.get()
        reg_raw = self.m_reg.get()

        # Check against both standard Arabic and reshaped display versions of 'شمال'
        if "شمال" in reg_raw or "ﺷﻤﺎﻝ" in reg_raw or "شمال" in render_ar(reg_raw):
            reg = "شمال"
        else:
            reg = "جنوب"

        m_c, n_c, tot = calculate_allowances(dep, ret, reg)

        self.m_meals.delete(0, 'end')
        self.m_meals.insert(0, str(m_c))
        self.m_nights.delete(0, 'end')
        self.m_nights.insert(0, str(n_c))

        self.temp_total = tot
        self.temp_text = tafqeet(tot)
        messagebox.showinfo("النتيجة", f"الإجمالي: {tot} دج\n{self.temp_text}")

    def save_mission(self):
        emp_str = self.m_emp_combo.get()
        emp_id = self.emp_map.get(emp_str)
        if not emp_id: return

        reg_raw = self.m_reg.get()
        if "شمال" in reg_raw or "ﺷﻤﺎﻝ" in reg_raw or "شمال" in render_ar(reg_raw):
            reg = "شمال"
        else:
            reg = "جنوب"

        # Support manual override
        try:
            m_c = int(self.m_meals.get())
            n_c = int(self.m_nights.get())
            rate = 800 if reg == "شمال" else 1000
            n_rate = 3200 if reg == "شمال" else 4000
            tot = (m_c * rate) + (n_c * n_rate)
            t_txt = tafqeet(tot)
        except:
            return

        data = {
            'budget_chapter': self.m_chap.get(),
            'budget_article': self.m_art.get(),
            'report_month_year': self.m_month.get(),
            'order_number': self.m_order.get(),
            'order_date': self.m_date.get(),
            'purpose': self.m_purp.get(),
            'itinerary': self.m_itin.get(),
            'transport_mode': self.m_trans.get(),
            'departure_datetime': self.m_dep.get(),
            'return_datetime': self.m_ret.get(),
            'region': reg,
            'meals_count': m_c,
            'nights_count': n_c,
            'total_amount': tot,
            'amount_text': t_txt
        }
        database.add_mission(emp_id, data)
        messagebox.showinfo("نجاح", "تم حفظ المهمة")
        self.refresh_mis_dropdown()

    def export_pdf(self):
        emp_str = self.m_emp_combo.get()
        emp_id = self.emp_map.get(emp_str)
        mis_str = self.export_combo.get()
        mis_id = self.mis_map.get(mis_str)

        if not emp_id or not mis_id: return

        emp = database.get_employee(emp_id)
        missions = database.get_missions_for_employee(emp_id)
        mission = next((m for m in missions if m[0] == mis_id), None)

        path, _ = filedialog.getSaveFileName(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if path:
            generate_pdf_report(emp, mission, path)
            messagebox.showinfo("نجاح", "تم التصدير بنجاح")

    def export_excel(self):
        emp_str = self.m_emp_combo.get()
        emp_id = self.emp_map.get(emp_str)
        mis_str = self.export_combo.get()
        mis_id = self.mis_map.get(mis_str)

        if not emp_id or not mis_id: return

        emp = database.get_employee(emp_id)
        missions = database.get_missions_for_employee(emp_id)
        mission = next((m for m in missions if m[0] == mis_id), None)

        path, _ = filedialog.getSaveFileName(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if path:
            generate_excel_report(emp, mission, path)
            messagebox.showinfo("نجاح", "تم التصدير بنجاح")

if __name__ == "__main__":
    app = MissionTrackApp()
    app.mainloop()
