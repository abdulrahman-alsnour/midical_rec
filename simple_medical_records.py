import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import json
from datetime import datetime
import os
from tkcalendar import DateEntry
import re

class SimpleMedicalRecord:
    def __init__(self, root):
        self.root = root
        self.root.title("Medical Records System")
        self.root.geometry("900x700")
        
        style = ttk.Style()
        style.configure('Title.TLabel', font=('Helvetica', 20, 'bold'))
        style.configure('Section.TLabelframe.Label', font=('Helvetica', 12, 'bold'))
        style.configure('Subsection.TLabelframe.Label', font=('Helvetica', 10, 'bold'))
        style.configure('TLabel', font=('Helvetica', 10))
        style.configure('TButton', font=('Helvetica', 10))
        style.configure('TEntry', font=('Helvetica', 10))
        
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        canvas = tk.Canvas(main_frame, bg='#f0f0f0')
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        title_frame = ttk.Frame(self.scrollable_frame)
        title_frame.pack(fill='x', pady=10)
        ttk.Label(title_frame, text="Medical Record Form", style='Title.TLabel').pack()
        
        personal_frame = ttk.LabelFrame(self.scrollable_frame, text="Personal Information", style='Section.TLabelframe', padding=15)
        personal_frame.pack(fill='x', pady=5)
        
        name_frame = ttk.Frame(personal_frame)
        name_frame.pack(fill='x', pady=5)
        ttk.Label(name_frame, text="Full Name *:").pack(anchor='w')
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(name_frame, textvariable=self.name_var, width=40)
        name_entry.pack(fill='x', pady=2)
        self.create_tooltip(name_entry, "Enter patient's full legal name")
        
        dob_frame = ttk.Frame(personal_frame)
        dob_frame.pack(fill='x', pady=5)
        ttk.Label(dob_frame, text="Date of Birth *:").pack(anchor='w')
        self.dob_calendar = DateEntry(dob_frame, width=20, background='darkblue',
                                    foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd',
                                    maxdate=datetime.now())
        self.dob_calendar.pack(fill='x', pady=2)
        self.create_tooltip(self.dob_calendar, "Select patient's date of birth")
        
        gender_frame = ttk.Frame(personal_frame)
        gender_frame.pack(fill='x', pady=5)
        ttk.Label(gender_frame, text="Gender *:").pack(anchor='w')
        self.gender_var = tk.StringVar(value="")
        for gender in ["Male", "Female", "Other"]:
            ttk.Radiobutton(gender_frame, text=gender, variable=self.gender_var, value=gender).pack(side='left', padx=10)
        
        contact_frame = ttk.LabelFrame(personal_frame, text="Contact Information", padding=10)
        contact_frame.pack(fill='x', pady=5)
        
        phone_frame = ttk.Frame(contact_frame)
        phone_frame.pack(fill='x', pady=5)
        ttk.Label(phone_frame, text="Phone:").pack(anchor='w')
        self.phone_var = tk.StringVar()
        phone_entry = ttk.Entry(phone_frame, textvariable=self.phone_var, width=20)
        phone_entry.pack(fill='x', pady=2)
        phone_entry.bind('<KeyRelease>', self.validate_phone)
        self.create_tooltip(phone_entry, "Enter phone number (digits only)")
        
        email_frame = ttk.Frame(contact_frame)
        email_frame.pack(fill='x', pady=5)
        ttk.Label(email_frame, text="Email:").pack(anchor='w')
        self.email_var = tk.StringVar()
        email_entry = ttk.Entry(email_frame, textvariable=self.email_var, width=40)
        email_entry.pack(fill='x', pady=2)
        email_entry.bind('<KeyRelease>', self.validate_email)
        self.create_tooltip(email_entry, "Enter valid email address")
        
        emergency_frame = ttk.LabelFrame(personal_frame, text="Emergency Contact", style='Subsection.TLabelframe', padding=10)
        emergency_frame.pack(fill='x', pady=5)
        
        emergency_name_frame = ttk.Frame(emergency_frame)
        emergency_name_frame.pack(fill='x', pady=5)
        ttk.Label(emergency_name_frame, text="Emergency Contact Name *:").pack(anchor='w')
        self.emergency_name_var = tk.StringVar()
        emergency_name_entry = ttk.Entry(emergency_name_frame, textvariable=self.emergency_name_var, width=40)
        emergency_name_entry.pack(fill='x', pady=2)
        self.create_tooltip(emergency_name_entry, "Enter full name of emergency contact")
        
        emergency_phone_frame = ttk.Frame(emergency_frame)
        emergency_phone_frame.pack(fill='x', pady=5)
        ttk.Label(emergency_phone_frame, text="Emergency Contact Phone *:").pack(anchor='w')
        self.emergency_phone_var = tk.StringVar()
        emergency_phone_entry = ttk.Entry(emergency_phone_frame, textvariable=self.emergency_phone_var, width=20)
        emergency_phone_entry.pack(fill='x', pady=2)
        emergency_phone_entry.bind('<KeyRelease>', self.validate_emergency_phone)
        self.create_tooltip(emergency_phone_entry, "Enter emergency contact's phone number (digits only)")
        
        emergency_relation_frame = ttk.Frame(emergency_frame)
        emergency_relation_frame.pack(fill='x', pady=5)
        ttk.Label(emergency_relation_frame, text="Relationship *:").pack(anchor='w')
        self.emergency_relation_var = tk.StringVar()
        emergency_relation_entry = ttk.Entry(emergency_relation_frame, textvariable=self.emergency_relation_var, width=40)
        emergency_relation_entry.pack(fill='x', pady=2)
        self.create_tooltip(emergency_relation_entry, "Enter relationship to patient (e.g., Spouse, Parent, Sibling)")
        
        insurance_frame = ttk.LabelFrame(personal_frame, text="Insurance Information", style='Subsection.TLabelframe', padding=10)
        insurance_frame.pack(fill='x', pady=5)
        
        insurance_provider_frame = ttk.Frame(insurance_frame)
        insurance_provider_frame.pack(fill='x', pady=5)
        ttk.Label(insurance_provider_frame, text="Insurance Provider *:").pack(anchor='w')
        self.insurance_provider_var = tk.StringVar()
        insurance_provider_entry = ttk.Entry(insurance_provider_frame, textvariable=self.insurance_provider_var, width=40)
        insurance_provider_entry.pack(fill='x', pady=2)
        self.create_tooltip(insurance_provider_entry, "Enter name of insurance provider")
        
        policy_number_frame = ttk.Frame(insurance_frame)
        policy_number_frame.pack(fill='x', pady=5)
        ttk.Label(policy_number_frame, text="Policy Number *:").pack(anchor='w')
        self.policy_number_var = tk.StringVar()
        policy_number_entry = ttk.Entry(policy_number_frame, textvariable=self.policy_number_var, width=40)
        policy_number_entry.pack(fill='x', pady=2)
        self.create_tooltip(policy_number_entry, "Enter insurance policy number")
        
        coverage_frame = ttk.Frame(insurance_frame)
        coverage_frame.pack(fill='x', pady=5)
        ttk.Label(coverage_frame, text="Coverage Details:").pack(anchor='w')
        self.coverage_text = scrolledtext.ScrolledText(coverage_frame, height=3, width=50, font=('Helvetica', 10))
        self.coverage_text.pack(fill='x', pady=2)
        self.create_tooltip(self.coverage_text, "Enter details about insurance coverage, limitations, or special conditions")
        
        medical_frame = ttk.LabelFrame(self.scrollable_frame, text="Medical Information", style='Section.TLabelframe', padding=15)
        medical_frame.pack(fill='x', pady=5)
        
        past_medical_frame = ttk.LabelFrame(medical_frame, text="Past Medical History", style='Subsection.TLabelframe', padding=10)
        past_medical_frame.pack(fill='x', pady=5)
        
        ttk.Label(past_medical_frame, text="Chronic Conditions:").pack(anchor='w')
        self.chronic_conditions_text = scrolledtext.ScrolledText(past_medical_frame, height=3, width=50, font=('Helvetica', 10))
        self.chronic_conditions_text.pack(fill='x', pady=2)
        self.create_tooltip(self.chronic_conditions_text, "List chronic conditions (e.g., diabetes, hypertension)")
        
        ttk.Label(past_medical_frame, text="Surgeries:").pack(anchor='w')
        self.surgeries_text = scrolledtext.ScrolledText(past_medical_frame, height=3, width=50, font=('Helvetica', 10))
        self.surgeries_text.pack(fill='x', pady=2)
        self.create_tooltip(self.surgeries_text, "List past surgeries with dates if known")
        
        ttk.Label(past_medical_frame, text="Hospitalizations:").pack(anchor='w')
        self.hospitalizations_text = scrolledtext.ScrolledText(past_medical_frame, height=3, width=50, font=('Helvetica', 10))
        self.hospitalizations_text.pack(fill='x', pady=2)
        self.create_tooltip(self.hospitalizations_text, "List significant hospitalizations with dates if known")
        
        family_history_frame = ttk.LabelFrame(medical_frame, text="Family Medical History", style='Subsection.TLabelframe', padding=10)
        family_history_frame.pack(fill='x', pady=5)
        
        ttk.Label(family_history_frame, text="Family Health Conditions:").pack(anchor='w')
        self.family_history_text = scrolledtext.ScrolledText(family_history_frame, height=4, width=50, font=('Helvetica', 10))
        self.family_history_text.pack(fill='x', pady=2)
        self.create_tooltip(self.family_history_text, "List health conditions of close relatives (parents, siblings) that may indicate genetic predispositions")
        
        social_history_frame = ttk.LabelFrame(medical_frame, text="Social History", style='Subsection.TLabelframe', padding=10)
        social_history_frame.pack(fill='x', pady=5)
        
        smoking_frame = ttk.Frame(social_history_frame)
        smoking_frame.pack(fill='x', pady=5)
        ttk.Label(smoking_frame, text="Smoking Status:").pack(side='left')
        self.smoking_var = tk.StringVar(value="")
        for status in ["Never", "Former", "Current"]:
            ttk.Radiobutton(smoking_frame, text=status, variable=self.smoking_var, value=status).pack(side='left', padx=10)
        
        alcohol_frame = ttk.Frame(social_history_frame)
        alcohol_frame.pack(fill='x', pady=5)
        ttk.Label(alcohol_frame, text="Alcohol Consumption:").pack(side='left')
        self.alcohol_var = tk.StringVar(value="")
        for status in ["None", "Occasional", "Regular"]:
            ttk.Radiobutton(alcohol_frame, text=status, variable=self.alcohol_var, value=status).pack(side='left', padx=10)
        
        drug_frame = ttk.Frame(social_history_frame)
        drug_frame.pack(fill='x', pady=5)
        ttk.Label(drug_frame, text="Drug Use:").pack(side='left')
        self.drug_var = tk.StringVar(value="")
        for status in ["None", "Past", "Current"]:
            ttk.Radiobutton(drug_frame, text=status, variable=self.drug_var, value=status).pack(side='left', padx=10)
        
        occupation_frame = ttk.Frame(social_history_frame)
        occupation_frame.pack(fill='x', pady=5)
        ttk.Label(occupation_frame, text="Occupation:").pack(anchor='w')
        self.occupation_var = tk.StringVar()
        occupation_entry = ttk.Entry(occupation_frame, textvariable=self.occupation_var, width=40)
        occupation_entry.pack(fill='x', pady=2)
        self.create_tooltip(occupation_entry, "Enter current or past occupation")
        
        ttk.Label(social_history_frame, text="Lifestyle Information:").pack(anchor='w')
        self.lifestyle_text = scrolledtext.ScrolledText(social_history_frame, height=4, width=50, font=('Helvetica', 10))
        self.lifestyle_text.pack(fill='x', pady=2)
        self.create_tooltip(self.lifestyle_text, "Enter information about diet, exercise habits, and living conditions")
        
        allergies_frame = ttk.LabelFrame(medical_frame, text="Allergies", style='Subsection.TLabelframe', padding=10)
        allergies_frame.pack(fill='x', pady=5)
        
        ttk.Label(allergies_frame, text="Known Allergies:").pack(anchor='w')
        self.allergies_text = scrolledtext.ScrolledText(allergies_frame, height=4, width=50, font=('Helvetica', 10))
        self.allergies_text.pack(fill='x', pady=2)
        self.create_tooltip(self.allergies_text, "List all known allergies to medications, foods, or environmental factors")
        
        immunization_frame = ttk.LabelFrame(medical_frame, text="Immunization Records", style='Subsection.TLabelframe', padding=10)
        immunization_frame.pack(fill='x', pady=5)
        
        ttk.Label(immunization_frame, text="Vaccination History:").pack(anchor='w')
        self.immunization_text = scrolledtext.ScrolledText(immunization_frame, height=4, width=50, font=('Helvetica', 10))
        self.immunization_text.pack(fill='x', pady=2)
        self.create_tooltip(self.immunization_text, "List vaccination history with dates and types of vaccines received")
        
        medications_frame = ttk.LabelFrame(medical_frame, text="Current Medications", style='Subsection.TLabelframe', padding=10)
        medications_frame.pack(fill='x', pady=5)
        
        ttk.Label(medications_frame, text="Medications:").pack(anchor='w')
        self.medications_text = scrolledtext.ScrolledText(medications_frame, height=4, width=50, font=('Helvetica', 10))
        self.medications_text.pack(fill='x', pady=2)
        self.create_tooltip(self.medications_text, "List all current medications with dosages and frequencies")
        
        vitals_frame = ttk.LabelFrame(self.scrollable_frame, text="Vital Signs", style='Section.TLabelframe', padding=15)
        vitals_frame.pack(fill='x', pady=5)
        
        bp_frame = ttk.LabelFrame(vitals_frame, text="Blood Pressure", style='Subsection.TLabelframe', padding=10)
        bp_frame.pack(fill='x', pady=5)
        
        systolic_frame = ttk.Frame(bp_frame)
        systolic_frame.pack(fill='x', pady=5)
        ttk.Label(systolic_frame, text="Systolic:").pack(side='left')
        self.bp_systolic_var = tk.StringVar()
        systolic_entry = ttk.Entry(systolic_frame, textvariable=self.bp_systolic_var, width=5)
        systolic_entry.pack(side='left', padx=5)
        systolic_entry.bind('<KeyRelease>', lambda e: self.validate_number(self.bp_systolic_var, 70, 200))
        
        systolic_dropdown = ttk.Combobox(systolic_frame, textvariable=self.bp_systolic_var, width=5, values=['90', '100', '110', '120', '130', '140', '150', '160', '170', '180'])
        systolic_dropdown.pack(side='left', padx=5)
        systolic_dropdown.bind('<<ComboboxSelected>>', lambda e: self.validate_number(self.bp_systolic_var, 70, 200))
        
        ttk.Label(systolic_frame, text="mmHg").pack(side='left', padx=5)
        
        diastolic_frame = ttk.Frame(bp_frame)
        diastolic_frame.pack(fill='x', pady=5)
        ttk.Label(diastolic_frame, text="Diastolic:").pack(side='left')
        self.bp_diastolic_var = tk.StringVar()
        diastolic_entry = ttk.Entry(diastolic_frame, textvariable=self.bp_diastolic_var, width=5)
        diastolic_entry.pack(side='left', padx=5)
        diastolic_entry.bind('<KeyRelease>', lambda e: self.validate_number(self.bp_diastolic_var, 40, 130))
        
        diastolic_dropdown = ttk.Combobox(diastolic_frame, textvariable=self.bp_diastolic_var, width=5, values=['50', '60', '70', '80', '90', '100', '110', '120'])
        diastolic_dropdown.pack(side='left', padx=5)
        diastolic_dropdown.bind('<<ComboboxSelected>>', lambda e: self.validate_number(self.bp_diastolic_var, 40, 130))
        
        ttk.Label(diastolic_frame, text="mmHg").pack(side='left', padx=5)
        
        hr_frame = ttk.LabelFrame(vitals_frame, text="Heart Rate", style='Subsection.TLabelframe', padding=10)
        hr_frame.pack(fill='x', pady=5)
        
        hr_input_frame = ttk.Frame(hr_frame)
        hr_input_frame.pack(fill='x', pady=5)
        
        hr_left_frame = ttk.Frame(hr_input_frame)
        hr_left_frame.pack(side='left', fill='x', expand=True)
        
        ttk.Label(hr_left_frame, text="Heart Rate:").pack(side='left')
        self.heart_rate_var = tk.StringVar()
        hr_entry = ttk.Entry(hr_left_frame, textvariable=self.heart_rate_var, width=5)
        hr_entry.pack(side='left', padx=5)
        hr_entry.bind('<KeyRelease>', lambda e: self.validate_heart_rate())
        
        hr_dropdown = ttk.Combobox(hr_left_frame, textvariable=self.heart_rate_var, width=5, 
                                 values=['60', '65', '70', '75', '80', '85', '90', '95', '100', '105', '110', '115', '120'])
        hr_dropdown.pack(side='left', padx=5)
        hr_dropdown.bind('<<ComboboxSelected>>', lambda e: self.validate_heart_rate())
        
        ttk.Label(hr_left_frame, text="bpm").pack(side='left', padx=5)
        
        hr_right_frame = ttk.Frame(hr_input_frame)
        hr_right_frame.pack(side='right', fill='x', expand=True)
        
        self.hr_status_var = tk.StringVar(value="")
        self.hr_status_label = ttk.Label(hr_right_frame, textvariable=self.hr_status_var)
        self.hr_status_label.pack(side='right')
        
        hr_range_frame = ttk.Frame(hr_frame)
        hr_range_frame.pack(fill='x', pady=5)
        
        range_vis_frame = ttk.Frame(hr_range_frame)
        range_vis_frame.pack(fill='x', pady=2)
        
        ttk.Label(range_vis_frame, text="40").pack(side='left')
        ttk.Label(range_vis_frame, text="60").pack(side='left', padx=20)
        ttk.Label(range_vis_frame, text="100").pack(side='left', padx=20)
        ttk.Label(range_vis_frame, text="200").pack(side='left')
        
        self.hr_canvas = tk.Canvas(range_vis_frame, height=20, bg='white')
        self.hr_canvas.pack(fill='x', padx=5)
        
        self.draw_heart_rate_range()
        
        ttk.Label(hr_frame, text="Normal range: 60-100 bpm", font=('Helvetica', 9, 'italic')).pack(pady=2)
        
        rr_frame = ttk.LabelFrame(vitals_frame, text="Respiratory Rate", style='Subsection.TLabelframe', padding=10)
        rr_frame.pack(fill='x', pady=5)
        
        rr_input_frame = ttk.Frame(rr_frame)
        rr_input_frame.pack(fill='x', pady=5)
        ttk.Label(rr_input_frame, text="Respiratory Rate:").pack(side='left')
        self.respiratory_rate_var = tk.StringVar()
        rr_entry = ttk.Entry(rr_input_frame, textvariable=self.respiratory_rate_var, width=5)
        rr_entry.pack(side='left', padx=5)
        rr_entry.bind('<KeyRelease>', lambda e: self.validate_number(self.respiratory_rate_var, 8, 40))
        
        rr_dropdown = ttk.Combobox(rr_input_frame, textvariable=self.respiratory_rate_var, width=5, values=['12', '14', '16', '18', '20', '22', '24'])
        rr_dropdown.pack(side='left', padx=5)
        rr_dropdown.bind('<<ComboboxSelected>>', lambda e: self.validate_number(self.respiratory_rate_var, 8, 40))
        
        ttk.Label(rr_input_frame, text="breaths/min").pack(side='left', padx=5)
        
        temp_frame = ttk.LabelFrame(vitals_frame, text="Temperature", style='Subsection.TLabelframe', padding=10)
        temp_frame.pack(fill='x', pady=5)
        
        temp_input_frame = ttk.Frame(temp_frame)
        temp_input_frame.pack(fill='x', pady=5)
        ttk.Label(temp_input_frame, text="Temperature:").pack(side='left')
        self.temperature_var = tk.StringVar()
        temp_entry = ttk.Entry(temp_input_frame, textvariable=self.temperature_var, width=5)
        temp_entry.pack(side='left', padx=5)
        temp_entry.bind('<KeyRelease>', lambda e: self.validate_number(self.temperature_var, 35, 42))
        
        temp_dropdown = ttk.Combobox(temp_input_frame, textvariable=self.temperature_var, width=5, values=['36.5', '37.0', '37.5', '38.0', '38.5', '39.0'])
        temp_dropdown.pack(side='left', padx=5)
        temp_dropdown.bind('<<ComboboxSelected>>', lambda e: self.validate_number(self.temperature_var, 35, 42))
        
        ttk.Label(temp_input_frame, text="°C").pack(side='left', padx=5)
        
        measurements_frame = ttk.LabelFrame(vitals_frame, text="Height and Weight", style='Subsection.TLabelframe', padding=10)
        measurements_frame.pack(fill='x', pady=5)
        
        height_frame = ttk.Frame(measurements_frame)
        height_frame.pack(fill='x', pady=5)
        ttk.Label(height_frame, text="Height:").pack(side='left')
        self.height_var = tk.StringVar()
        height_entry = ttk.Entry(height_frame, textvariable=self.height_var, width=5)
        height_entry.pack(side='left', padx=5)
        height_entry.bind('<KeyRelease>', lambda e: self.calculate_bmi())
        
        height_dropdown = ttk.Combobox(height_frame, textvariable=self.height_var, width=5, 
                                     values=['150', '155', '160', '165', '170', '175', '180', '185', '190'])
        height_dropdown.pack(side='left', padx=5)
        height_dropdown.bind('<<ComboboxSelected>>', lambda e: self.calculate_bmi())
        
        ttk.Label(height_frame, text="cm").pack(side='left', padx=5)
        
        weight_frame = ttk.Frame(measurements_frame)
        weight_frame.pack(fill='x', pady=5)
        ttk.Label(weight_frame, text="Weight:").pack(side='left')
        self.weight_var = tk.StringVar()
        weight_entry = ttk.Entry(weight_frame, textvariable=self.weight_var, width=5)
        weight_entry.pack(side='left', padx=5)
        weight_entry.bind('<KeyRelease>', lambda e: self.calculate_bmi())
        
        weight_dropdown = ttk.Combobox(weight_frame, textvariable=self.weight_var, width=5, 
                                     values=['50', '55', '60', '65', '70', '75', '80', '85', '90'])
        weight_dropdown.pack(side='left', padx=5)
        weight_dropdown.bind('<<ComboboxSelected>>', lambda e: self.calculate_bmi())
        
        ttk.Label(weight_frame, text="kg").pack(side='left', padx=5)
        
        bmi_frame = ttk.Frame(measurements_frame)
        bmi_frame.pack(fill='x', pady=5)
        
        bmi_value_frame = ttk.Frame(bmi_frame)
        bmi_value_frame.pack(fill='x', pady=2)
        
        ttk.Label(bmi_value_frame, text="BMI:").pack(side='left')
        self.bmi_var = tk.StringVar()
        self.bmi_label = ttk.Label(bmi_value_frame, textvariable=self.bmi_var)
        self.bmi_label.pack(side='left', padx=5)
        
        ttk.Label(bmi_value_frame, text="Category:").pack(side='left', padx=(20, 5))
        self.bmi_category_var = tk.StringVar()
        self.bmi_category_combo = ttk.Combobox(bmi_value_frame, textvariable=self.bmi_category_var, 
                                              values=['Underweight (<18.5)', 'Normal (18.5-24.9)', 
                                                     'Overweight (25-29.9)', 'Obese (≥30)'],
                                              state='readonly', width=20)
        self.bmi_category_combo.pack(side='left', padx=5)
        self.bmi_category_combo.bind('<<ComboboxSelected>>', self.update_bmi_from_category)
        
        bmi_range_frame = ttk.Frame(bmi_frame)
        bmi_range_frame.pack(fill='x', pady=2)
        
        ttk.Label(bmi_range_frame, text="Underweight\n<18.5").pack(side='left')
        ttk.Label(bmi_range_frame, text="Normal\n18.5-24.9").pack(side='left', padx=20)
        ttk.Label(bmi_range_frame, text="Overweight\n25-29.9").pack(side='left', padx=20)
        ttk.Label(bmi_range_frame, text="Obese\n≥30").pack(side='left')
        
        self.bmi_canvas = tk.Canvas(bmi_range_frame, height=20, bg='white')
        self.bmi_canvas.pack(fill='x', padx=5)
        
        self.draw_bmi_range()
        
        notes_frame = ttk.LabelFrame(self.scrollable_frame, text="Additional Notes", style='Section.TLabelframe', padding=15)
        notes_frame.pack(fill='x', pady=5)
        
        self.notes_text = scrolledtext.ScrolledText(notes_frame, height=4, width=50, font=('Helvetica', 10))
        self.notes_text.pack(fill='x', pady=2)
        self.create_tooltip(self.notes_text, "Enter any additional notes or observations")
        
        physical_exam_frame = ttk.LabelFrame(self.scrollable_frame, text="Physical Examination", style='Section.TLabelframe', padding=15)
        physical_exam_frame.pack(fill='x', pady=5)
        
        general_frame = ttk.LabelFrame(physical_exam_frame, text="General Appearance", style='Subsection.TLabelframe', padding=10)
        general_frame.pack(fill='x', pady=5)
        
        ttk.Label(general_frame, text="General Appearance:").pack(anchor='w')
        self.general_appearance_text = scrolledtext.ScrolledText(general_frame, height=3, width=50, font=('Helvetica', 10))
        self.general_appearance_text.pack(fill='x', pady=2)
        self.create_tooltip(self.general_appearance_text, "Document patient's general appearance, level of consciousness, and overall presentation")
        
        heent_frame = ttk.LabelFrame(physical_exam_frame, text="HEENT", style='Subsection.TLabelframe', padding=10)
        heent_frame.pack(fill='x', pady=5)
        
        head_frame = ttk.Frame(heent_frame)
        head_frame.pack(fill='x', pady=5)
        ttk.Label(head_frame, text="Head:").pack(anchor='w')
        self.head_text = scrolledtext.ScrolledText(head_frame, height=2, width=50, font=('Helvetica', 10))
        self.head_text.pack(fill='x', pady=2)
        
        eyes_frame = ttk.Frame(heent_frame)
        eyes_frame.pack(fill='x', pady=5)
        ttk.Label(eyes_frame, text="Eyes:").pack(anchor='w')
        self.eyes_text = scrolledtext.ScrolledText(eyes_frame, height=2, width=50, font=('Helvetica', 10))
        self.eyes_text.pack(fill='x', pady=2)
        
        
        ears_frame = ttk.Frame(heent_frame)
        ears_frame.pack(fill='x', pady=5)
        ttk.Label(ears_frame, text="Ears:").pack(anchor='w')
        self.ears_text = scrolledtext.ScrolledText(ears_frame, height=2, width=50, font=('Helvetica', 10))
        self.ears_text.pack(fill='x', pady=2)
        
        nose_frame = ttk.Frame(heent_frame)
        nose_frame.pack(fill='x', pady=5)
        ttk.Label(nose_frame, text="Nose:").pack(anchor='w')
        self.nose_text = scrolledtext.ScrolledText(nose_frame, height=2, width=50, font=('Helvetica', 10))
        self.nose_text.pack(fill='x', pady=2)
        
        throat_frame = ttk.Frame(heent_frame)
        throat_frame.pack(fill='x', pady=5)
        ttk.Label(throat_frame, text="Throat:").pack(anchor='w')
        self.throat_text = scrolledtext.ScrolledText(throat_frame, height=2, width=50, font=('Helvetica', 10))
        self.throat_text.pack(fill='x', pady=2)
        
        cv_frame = ttk.LabelFrame(physical_exam_frame, text="Cardiovascular System", style='Subsection.TLabelframe', padding=10)
        cv_frame.pack(fill='x', pady=5)
        
        ttk.Label(cv_frame, text="Cardiovascular Findings:").pack(anchor='w')
        self.cv_text = scrolledtext.ScrolledText(cv_frame, height=3, width=50, font=('Helvetica', 10))
        self.cv_text.pack(fill='x', pady=2)
        self.create_tooltip(self.cv_text, "Document heart sounds, pulses, edema, and other cardiovascular findings")
        
        resp_frame = ttk.LabelFrame(physical_exam_frame, text="Respiratory System", style='Subsection.TLabelframe', padding=10)
        resp_frame.pack(fill='x', pady=5)
        
        ttk.Label(resp_frame, text="Respiratory Findings:").pack(anchor='w')
        self.resp_text = scrolledtext.ScrolledText(resp_frame, height=3, width=50, font=('Helvetica', 10))
        self.resp_text.pack(fill='x', pady=2)
        self.create_tooltip(self.resp_text, "Document breath sounds, respiratory effort, and other respiratory findings")
        
        abdomen_frame = ttk.LabelFrame(physical_exam_frame, text="Abdomen", style='Subsection.TLabelframe', padding=10)
        abdomen_frame.pack(fill='x', pady=5)
        
        ttk.Label(abdomen_frame, text="Abdominal Findings:").pack(anchor='w')
        self.abdomen_text = scrolledtext.ScrolledText(abdomen_frame, height=3, width=50, font=('Helvetica', 10))
        self.abdomen_text.pack(fill='x', pady=2)
        self.create_tooltip(self.abdomen_text, "Document abdominal exam findings, including tenderness, masses, and organomegaly")
        
        msk_frame = ttk.LabelFrame(physical_exam_frame, text="Musculoskeletal System", style='Subsection.TLabelframe', padding=10)
        msk_frame.pack(fill='x', pady=5)
        
        ttk.Label(msk_frame, text="Musculoskeletal Findings:").pack(anchor='w')
        self.msk_text = scrolledtext.ScrolledText(msk_frame, height=3, width=50, font=('Helvetica', 10))
        self.msk_text.pack(fill='x', pady=2)
        self.create_tooltip(self.msk_text, "Document joint range of motion, strength, and other musculoskeletal findings")
        
        neuro_frame = ttk.LabelFrame(physical_exam_frame, text="Neurological Assessment", style='Subsection.TLabelframe', padding=10)
        neuro_frame.pack(fill='x', pady=5)
        
        ttk.Label(neuro_frame, text="Neurological Findings:").pack(anchor='w')
        self.neuro_text = scrolledtext.ScrolledText(neuro_frame, height=3, width=50, font=('Helvetica', 10))
        self.neuro_text.pack(fill='x', pady=2)
        self.create_tooltip(self.neuro_text, "Document neurological exam findings, including mental status, cranial nerves, and motor/sensory function")
        
        diagnostic_frame = ttk.LabelFrame(self.scrollable_frame, text="Diagnostic Tests and Results", style='Section.TLabelframe', padding=15)
        diagnostic_frame.pack(fill='x', pady=5)
        
        lab_frame = ttk.LabelFrame(diagnostic_frame, text="Laboratory Tests", style='Subsection.TLabelframe', padding=10)
        lab_frame.pack(fill='x', pady=5)
        
        lab_test_frame = ttk.Frame(lab_frame)
        lab_test_frame.pack(fill='x', pady=5)
        ttk.Label(lab_test_frame, text="Select Test:").pack(side='left')
        self.lab_test_var = tk.StringVar()
        lab_test_combo = ttk.Combobox(lab_test_frame, textvariable=self.lab_test_var, 
                                    values=['Complete Blood Count (CBC)', 'Basic Metabolic Panel (BMP)', 
                                           'Comprehensive Metabolic Panel (CMP)', 'Lipid Panel',
                                           'Thyroid Function Tests', 'Urinalysis', 'Other'],
                                    state='readonly', width=30)
        lab_test_combo.pack(side='left', padx=5)
        lab_test_combo.bind('<<ComboboxSelected>>', self.on_lab_test_selected)
        
        lab_date_frame = ttk.Frame(lab_frame)
        lab_date_frame.pack(fill='x', pady=5)
        ttk.Label(lab_date_frame, text="Date:").pack(side='left')
        self.lab_date_calendar = DateEntry(lab_date_frame, width=20, background='darkblue',
                                         foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.lab_date_calendar.pack(side='left', padx=5)
        
        lab_results_frame = ttk.Frame(lab_frame)
        lab_results_frame.pack(fill='x', pady=5)
        ttk.Label(lab_results_frame, text="Results:").pack(anchor='w')
        self.lab_results_text = scrolledtext.ScrolledText(lab_results_frame, height=3, width=50, font=('Helvetica', 10))
        self.lab_results_text.pack(fill='x', pady=2)
        
        lab_buttons_frame = ttk.Frame(lab_frame)
        lab_buttons_frame.pack(fill='x', pady=5)
        ttk.Button(lab_buttons_frame, text="Add Test", command=self.add_lab_test).pack(side='left', padx=5)
        ttk.Button(lab_buttons_frame, text="Remove Last", command=self.remove_last_lab_test).pack(side='left', padx=5)
        
        imaging_frame = ttk.LabelFrame(diagnostic_frame, text="Imaging Studies", style='Subsection.TLabelframe', padding=10)
        imaging_frame.pack(fill='x', pady=5)
        
        imaging_type_frame = ttk.Frame(imaging_frame)
        imaging_type_frame.pack(fill='x', pady=5)
        ttk.Label(imaging_type_frame, text="Type:").pack(side='left')
        self.imaging_type_var = tk.StringVar()
        imaging_type_combo = ttk.Combobox(imaging_type_frame, textvariable=self.imaging_type_var,
                                        values=['X-ray', 'MRI', 'CT Scan', 'Ultrasound', 'Other'],
                                        state='readonly', width=20)
        imaging_type_combo.pack(side='left', padx=5)
        
        body_part_frame = ttk.Frame(imaging_frame)
        body_part_frame.pack(fill='x', pady=5)
        ttk.Label(body_part_frame, text="Body Part/Area:").pack(side='left')
        self.body_part_var = tk.StringVar()
        body_part_entry = ttk.Entry(body_part_frame, textvariable=self.body_part_var, width=30)
        body_part_entry.pack(side='left', padx=5)
        
        imaging_date_frame = ttk.Frame(imaging_frame)
        imaging_date_frame.pack(fill='x', pady=5)
        ttk.Label(imaging_date_frame, text="Date:").pack(side='left')
        self.imaging_date_calendar = DateEntry(imaging_date_frame, width=20, background='darkblue',
                                             foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.imaging_date_calendar.pack(side='left', padx=5)
        
        imaging_findings_frame = ttk.Frame(imaging_frame)
        imaging_findings_frame.pack(fill='x', pady=5)
        ttk.Label(imaging_findings_frame, text="Findings:").pack(anchor='w')
        self.imaging_findings_text = scrolledtext.ScrolledText(imaging_findings_frame, height=3, width=50, font=('Helvetica', 10))
        self.imaging_findings_text.pack(fill='x', pady=2)
        
        imaging_buttons_frame = ttk.Frame(imaging_frame)
        imaging_buttons_frame.pack(fill='x', pady=5)
        ttk.Button(imaging_buttons_frame, text="Add Study", command=self.add_imaging_study).pack(side='left', padx=5)
        ttk.Button(imaging_buttons_frame, text="Remove Last", command=self.remove_last_imaging_study).pack(side='left', padx=5)
        
        biopsy_frame = ttk.LabelFrame(diagnostic_frame, text="Biopsy Results", style='Subsection.TLabelframe', padding=10)
        biopsy_frame.pack(fill='x', pady=5)
        
        biopsy_type_frame = ttk.Frame(biopsy_frame)
        biopsy_type_frame.pack(fill='x', pady=5)
        ttk.Label(biopsy_type_frame, text="Type:").pack(side='left')
        self.biopsy_type_var = tk.StringVar()
        biopsy_type_combo = ttk.Combobox(biopsy_type_frame, textvariable=self.biopsy_type_var,
                                       values=['Needle Biopsy', 'Surgical Biopsy', 'Endoscopic Biopsy', 'Other'],
                                       state='readonly', width=20)
        biopsy_type_combo.pack(side='left', padx=5)
        
        biopsy_site_frame = ttk.Frame(biopsy_frame)
        biopsy_site_frame.pack(fill='x', pady=5)
        ttk.Label(biopsy_site_frame, text="Site:").pack(side='left')
        self.biopsy_site_var = tk.StringVar()
        biopsy_site_entry = ttk.Entry(biopsy_site_frame, textvariable=self.biopsy_site_var, width=30)
        biopsy_site_entry.pack(side='left', padx=5)
        
        biopsy_date_frame = ttk.Frame(biopsy_frame)
        biopsy_date_frame.pack(fill='x', pady=5)
        ttk.Label(biopsy_date_frame, text="Date:").pack(side='left')
        self.biopsy_date_calendar = DateEntry(biopsy_date_frame, width=20, background='darkblue',
                                            foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.biopsy_date_calendar.pack(side='left', padx=5)
        
        biopsy_results_frame = ttk.Frame(biopsy_frame)
        biopsy_results_frame.pack(fill='x', pady=5)
        ttk.Label(biopsy_results_frame, text="Results:").pack(anchor='w')
        self.biopsy_results_text = scrolledtext.ScrolledText(biopsy_results_frame, height=3, width=50, font=('Helvetica', 10))
        self.biopsy_results_text.pack(fill='x', pady=2)
        
        biopsy_buttons_frame = ttk.Frame(biopsy_frame)
        biopsy_buttons_frame.pack(fill='x', pady=5)
        ttk.Button(biopsy_buttons_frame, text="Add Biopsy", command=self.add_biopsy).pack(side='left', padx=5)
        ttk.Button(biopsy_buttons_frame, text="Remove Last", command=self.remove_last_biopsy).pack(side='left', padx=5)
        
        ecg_frame = ttk.LabelFrame(diagnostic_frame, text="ECG/EKG Results", style='Subsection.TLabelframe', padding=10)
        ecg_frame.pack(fill='x', pady=5)
        
        ecg_date_frame = ttk.Frame(ecg_frame)
        ecg_date_frame.pack(fill='x', pady=5)
        ttk.Label(ecg_date_frame, text="Date:").pack(side='left')
        self.ecg_date_calendar = DateEntry(ecg_date_frame, width=20, background='darkblue',
                                         foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.ecg_date_calendar.pack(side='left', padx=5)
        
        ecg_type_frame = ttk.Frame(ecg_frame)
        ecg_type_frame.pack(fill='x', pady=5)
        ttk.Label(ecg_type_frame, text="Type:").pack(side='left')
        self.ecg_type_var = tk.StringVar()
        ecg_type_combo = ttk.Combobox(ecg_type_frame, textvariable=self.ecg_type_var,
                                    values=['Resting ECG', 'Stress Test ECG', 'Holter Monitor', 'Event Monitor'],
                                    state='readonly', width=20)
        ecg_type_combo.pack(side='left', padx=5)
        
        ecg_results_frame = ttk.Frame(ecg_frame)
        ecg_results_frame.pack(fill='x', pady=5)
        ttk.Label(ecg_results_frame, text="Results:").pack(anchor='w')
        self.ecg_results_text = scrolledtext.ScrolledText(ecg_results_frame, height=3, width=50, font=('Helvetica', 10))
        self.ecg_results_text.pack(fill='x', pady=2)
        
        ecg_buttons_frame = ttk.Frame(ecg_frame)
        ecg_buttons_frame.pack(fill='x', pady=5)
        ttk.Button(ecg_buttons_frame, text="Add ECG", command=self.add_ecg).pack(side='left', padx=5)
        ttk.Button(ecg_buttons_frame, text="Remove Last", command=self.remove_last_ecg).pack(side='left', padx=5)
        
        other_tests_frame = ttk.LabelFrame(diagnostic_frame, text="Other Specialized Tests", style='Subsection.TLabelframe', padding=10)
        other_tests_frame.pack(fill='x', pady=5)
        
        other_test_type_frame = ttk.Frame(other_tests_frame)
        other_test_type_frame.pack(fill='x', pady=5)
        ttk.Label(other_test_type_frame, text="Test Type:").pack(side='left')
        self.other_test_type_var = tk.StringVar()
        other_test_type_combo = ttk.Combobox(other_test_type_frame, textvariable=self.other_test_type_var,
                                           values=['Pulmonary Function Test', 'Sleep Study', 'Allergy Test',
                                                  'Genetic Test', 'Other'],
                                           state='readonly', width=20)
        other_test_type_combo.pack(side='left', padx=5)
        
        
        other_test_date_frame = ttk.Frame(other_tests_frame)
        other_test_date_frame.pack(fill='x', pady=5)
        ttk.Label(other_test_date_frame, text="Date:").pack(side='left')
        self.other_test_date_calendar = DateEntry(other_test_date_frame, width=20, background='darkblue',
                                                foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.other_test_date_calendar.pack(side='left', padx=5)
        
        other_test_results_frame = ttk.Frame(other_tests_frame)
        other_test_results_frame.pack(fill='x', pady=5)
        ttk.Label(other_test_results_frame, text="Results:").pack(anchor='w')
        self.other_test_results_text = scrolledtext.ScrolledText(other_test_results_frame, height=3, width=50, font=('Helvetica', 10))
        self.other_test_results_text.pack(fill='x', pady=2)
        
        other_test_buttons_frame = ttk.Frame(other_tests_frame)
        other_test_buttons_frame.pack(fill='x', pady=5)
        ttk.Button(other_test_buttons_frame, text="Add Test", command=self.add_other_test).pack(side='left', padx=5)
        ttk.Button(other_test_buttons_frame, text="Remove Last", command=self.remove_last_other_test).pack(side='left', padx=5)
        
        self.lab_tests = []
        self.imaging_studies = []
        self.biopsies = []
        self.ecg_results = []
        self.other_tests = []
        
        button_frame = ttk.Frame(self.scrollable_frame)
        button_frame.pack(pady=20)
        
        save_button = ttk.Button(button_frame, text="Save Record", command=self.save_record)
        save_button.pack(side='left', padx=5)
        self.create_tooltip(save_button, "Save the medical record")
        
        clear_button = ttk.Button(button_frame, text="Clear Form", command=self.clear_form)
        clear_button.pack(side='left', padx=5)
        self.create_tooltip(clear_button, "Clear all fields and start over")
        
        self.records_dir = "medical_records"
        if not os.path.exists(self.records_dir):
            os.makedirs(self.records_dir)
    
    def create_tooltip(self, widget, text):
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = ttk.Label(tooltip, text=text, background="#ffffe0", relief='solid', borderwidth=1)
            label.pack()
            
            def hide_tooltip():
                tooltip.destroy()
            
            widget.tooltip = tooltip
            widget.bind('<Leave>', lambda e: hide_tooltip())
        
        widget.bind('<Enter>', show_tooltip)
    
    def validate_phone(self, event=None):
        phone = self.phone_var.get()
        if phone:
            phone = re.sub(r'\D', '', phone)
            if len(phone) > 10:
                phone = phone[:10]
            self.phone_var.set(phone)
    
    def validate_emergency_phone(self, event=None):
        phone = self.emergency_phone_var.get()
        if phone:
            phone = re.sub(r'\D', '', phone)
            if len(phone) > 10:
                phone = phone[:10]
            self.emergency_phone_var.set(phone)
    
    def validate_email(self, event=None):
        email = self.email_var.get()
        if email:
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(pattern, email):
                self.email_var.set(email)
                self.create_tooltip(self.email_entry, "Please enter a valid email address (e.g., example@domain.com)")
            else:
                self.create_tooltip(self.email_entry, "Valid email address")
    
    def validate_number(self, var, min_val, max_val):
        try:
            value = float(var.get())
            if value < min_val or value > max_val:
                var.set("")
        except ValueError:
            if var.get() != "":
                var.set("")
    
    def calculate_bmi(self):
        try:
            height = float(self.height_var.get())
            weight = float(self.weight_var.get())
            if height > 0 and weight > 0:
                height_m = height / 100
                bmi = weight / (height_m * height_m)
                self.bmi_var.set(f"{bmi:.1f}")
                
                if bmi < 18.5:
                    category = "Underweight (<18.5)"
                    color = 'blue'
                elif bmi < 25:
                    category = "Normal (18.5-24.9)"
                    color = 'green'
                elif bmi < 30:
                    category = "Overweight (25-29.9)"
                    color = 'orange'
                else:
                    category = "Obese (≥30)"
                    color = 'red'
                
                self.bmi_category_var.set(category)
                self.bmi_category_label.configure(foreground=color)
                
                self.update_bmi_indicator(bmi)
            else:
                self.bmi_var.set("")
                self.bmi_category_var.set("")
        except ValueError:
            self.bmi_var.set("")
            self.bmi_category_var.set("")
    
    def validate_heart_rate(self):
        try:
            value = float(self.heart_rate_var.get())
            if 40 <= value <= 200:
                if value < 60:
                    self.hr_status_var.set("Bradycardia")
                    self.hr_status_label.configure(foreground='blue')
                elif value > 100:
                    self.hr_status_var.set("Tachycardia")
                    self.hr_status_label.configure(foreground='red')
                else:
                    self.hr_status_var.set("Normal")
                    self.hr_status_label.configure(foreground='green')
                
                self.update_heart_rate_indicator(value)
            else:
                self.heart_rate_var.set("")
                self.hr_status_var.set("")
        except ValueError:
            if self.heart_rate_var.get() != "":
                self.heart_rate_var.set("")
            self.hr_status_var.set("")
    
    def draw_heart_rate_range(self):
        canvas = self.hr_canvas
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        
        normal_start = (60 - 40) / 160 * width
        normal_end = (100 - 40) / 160 * width
        canvas.create_rectangle(normal_start, 0, normal_end, height, fill='lightgreen')
        
        canvas.create_line(0, height/2, width, height/2, fill='black')
    
    def update_heart_rate_indicator(self, value):
        canvas = self.hr_canvas
        width = canvas.winfo_width()
        
        canvas.delete('indicator')
        
        position = (value - 40) / 160 * width
        
        canvas.create_line(position, 0, position, canvas.winfo_height(), 
                          fill='red', width=2, tags='indicator')
    
    def draw_bmi_range(self):
        canvas = self.bmi_canvas
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        
        ranges = [
            (0, 18.5, 'lightblue'),    
            (18.5, 25, 'lightgreen'),  
            (25, 30, '#FFA07A'),       
            (30, 40, 'lightpink')      
        ]
        
        for start, end, color in ranges:
            start_pos = (start / 40) * width
            end_pos = (end / 40) * width
            canvas.create_rectangle(start_pos, 0, end_pos, height, fill=color)
        
        canvas.create_line(0, height/2, width, height/2, fill='black')
    
    def update_bmi_indicator(self, value):
        canvas = self.bmi_canvas
        width = canvas.winfo_width()
        
        canvas.delete('indicator')
        
        position = (value / 40) * width
        
        canvas.create_line(position, 0, position, canvas.winfo_height(), 
                          fill='red', width=2, tags='indicator')
    
    def update_bmi_from_category(self, event=None):
        category = self.bmi_category_var.get()
        if category:
            if category == 'Underweight (<18.5)':
                self.bmi_var.set("18.0")
                self.bmi_category_label.configure(foreground='blue')
            elif category == 'Normal (18.5-24.9)':
                self.bmi_var.set("22.0")
                self.bmi_category_label.configure(foreground='green')
            elif category == 'Overweight (25-29.9)':
                self.bmi_var.set("27.0")
                self.bmi_category_label.configure(foreground='orange')
            elif category == 'Obese (≥30)':
                self.bmi_var.set("32.0")
                self.bmi_category_label.configure(foreground='red')
            
            self.update_bmi_indicator(float(self.bmi_var.get()))
    
    def on_lab_test_selected(self, event=None):
        test = self.lab_test_var.get()
        if test == 'Other':
            self.lab_test_custom_var = tk.StringVar()
            custom_entry = ttk.Entry(self.lab_test_frame, textvariable=self.lab_test_custom_var, width=30)
            custom_entry.pack(side='left', padx=5)
            custom_entry.focus()
    
    def add_lab_test(self):
        test = {
            'type': self.lab_test_var.get(),
            'date': self.lab_date_calendar.get_date().strftime("%Y-%m-%d"),
            'results': self.lab_results_text.get("1.0", tk.END).strip()
        }
        self.lab_tests.append(test)
        self.clear_lab_test_fields()
    
    def remove_last_lab_test(self):
        if self.lab_tests:
            self.lab_tests.pop()
    
    def add_imaging_study(self):
        study = {
            'type': self.imaging_type_var.get(),
            'body_part': self.body_part_var.get(),
            'date': self.imaging_date_calendar.get_date().strftime("%Y-%m-%d"),
            'findings': self.imaging_findings_text.get("1.0", tk.END).strip()
        }
        self.imaging_studies.append(study)
        self.clear_imaging_fields()
    
    def remove_last_imaging_study(self):
        if self.imaging_studies:
            self.imaging_studies.pop()
    
    def add_biopsy(self):
        biopsy = {
            'type': self.biopsy_type_var.get(),
            'site': self.biopsy_site_var.get(),
            'date': self.biopsy_date_calendar.get_date().strftime("%Y-%m-%d"),
            'results': self.biopsy_results_text.get("1.0", tk.END).strip()
        }
        self.biopsies.append(biopsy)
        self.clear_biopsy_fields()
    
    def remove_last_biopsy(self):
        if self.biopsies:
            self.biopsies.pop()
    
    def add_ecg(self):
        ecg = {
            'type': self.ecg_type_var.get(),
            'date': self.ecg_date_calendar.get_date().strftime("%Y-%m-%d"),
            'results': self.ecg_results_text.get("1.0", tk.END).strip()
        }
        self.ecg_results.append(ecg)
        self.clear_ecg_fields()
    
    def remove_last_ecg(self):
        if self.ecg_results:
            self.ecg_results.pop()
    
    def add_other_test(self):
        test = {
            'type': self.other_test_type_var.get(),
            'date': self.other_test_date_calendar.get_date().strftime("%Y-%m-%d"),
            'results': self.other_test_results_text.get("1.0", tk.END).strip()
        }
        self.other_tests.append(test)
        self.clear_other_test_fields()
    
    def remove_last_other_test(self):
        if self.other_tests:
            self.other_tests.pop()
    
    def clear_lab_test_fields(self):
        self.lab_test_var.set("")
        self.lab_date_calendar.set_date(datetime.now())
        self.lab_results_text.delete("1.0", tk.END)
    
    def clear_imaging_fields(self):
        self.imaging_type_var.set("")
        self.body_part_var.set("")
        self.imaging_date_calendar.set_date(datetime.now())
        self.imaging_findings_text.delete("1.0", tk.END)
    
    def clear_biopsy_fields(self):
        self.biopsy_type_var.set("")
        self.biopsy_site_var.set("")
        self.biopsy_date_calendar.set_date(datetime.now())
        self.biopsy_results_text.delete("1.0", tk.END)
    
    def clear_ecg_fields(self):
        self.ecg_type_var.set("")
        self.ecg_date_calendar.set_date(datetime.now())
        self.ecg_results_text.delete("1.0", tk.END)
    
    def clear_other_test_fields(self):
        self.other_test_type_var.set("")
        self.other_test_date_calendar.set_date(datetime.now())
        self.other_test_results_text.delete("1.0", tk.END)
    
    def save_record(self):
        required_fields = {
            "Full Name": self.name_var.get().strip(),
            "Date of Birth": self.dob_calendar.get_date().strftime("%Y-%m-%d"),
            "Gender": self.gender_var.get(),
            "Phone": self.phone_var.get().strip(),
            "Email": self.email_var.get().strip(),
            "Emergency Contact Name": self.emergency_name_var.get().strip(),
            "Emergency Contact Phone": self.emergency_phone_var.get().strip(),
            "Emergency Contact Relationship": self.emergency_relation_var.get().strip(),
            "Insurance Provider": self.insurance_provider_var.get().strip(),
            "Insurance ID": self.policy_number_var.get().strip()
        }
        
        missing_fields = [field for field, value in required_fields.items() if not value]
        if missing_fields:
            messagebox.showerror("Error", f"Please fill in the following required fields:\n{', '.join(missing_fields)}")
            return
        
        record = {
            "personal_info": {
                "name": self.name_var.get().strip(),
                "dob": self.dob_calendar.get_date().strftime("%Y-%m-%d"),
                "gender": self.gender_var.get(),
                "phone": self.phone_var.get().strip(),
                "email": self.email_var.get().strip(),
                "emergency_contact": {
                    "name": self.emergency_name_var.get().strip(),
                    "phone": self.emergency_phone_var.get().strip(),
                    "relationship": self.emergency_relation_var.get().strip()
                },
                "insurance": {
                    "provider": self.insurance_provider_var.get().strip(),
                    "id": self.policy_number_var.get().strip(),
                    "group_number": self.coverage_text.get("1.0", tk.END).strip()
                }
            },
            "medical_info": {
                "past_medical": {
                    "chronic_conditions": self.chronic_conditions_text.get("1.0", tk.END).strip(),
                    "surgeries": self.surgeries_text.get("1.0", tk.END).strip(),
                    "hospitalizations": self.hospitalizations_text.get("1.0", tk.END).strip()
                },
                "family_history": self.family_history_text.get("1.0", tk.END).strip(),
                "social_history": {
                    "smoking": self.smoking_var.get(),
                    "alcohol": self.alcohol_var.get(),
                    "drug_use": self.drug_var.get(),
                    "occupation": self.occupation_var.get(),
                    "lifestyle": self.lifestyle_text.get("1.0", tk.END).strip()
                },
                "allergies": self.allergies_text.get("1.0", tk.END).strip(),
                "immunizations": self.immunization_text.get("1.0", tk.END).strip(),
                "medications": self.medications_text.get("1.0", tk.END).strip()
            },
            "vital_signs": {
                "blood_pressure": {
                    "systolic": self.bp_systolic_var.get(),
                    "diastolic": self.bp_diastolic_var.get()
                },
                "heart_rate": self.heart_rate_var.get(),
                "respiratory_rate": self.respiratory_rate_var.get(),
                "temperature": self.temperature_var.get(),
                "height": self.height_var.get(),
                "weight": self.weight_var.get(),
                "bmi": self.bmi_var.get(),
                "bmi_category": self.bmi_category_var.get().strip('()')
            },
            "physical_examination": {
                "general_appearance": self.general_appearance_text.get("1.0", tk.END).strip(),
                "heent": {
                    "head": self.head_text.get("1.0", tk.END).strip(),
                    "eyes": self.eyes_text.get("1.0", tk.END).strip(),
                    "ears": self.ears_text.get("1.0", tk.END).strip(),
                    "nose": self.nose_text.get("1.0", tk.END).strip(),
                    "throat": self.throat_text.get("1.0", tk.END).strip()
                },
                "cardiovascular": self.cv_text.get("1.0", tk.END).strip(),
                "respiratory": self.resp_text.get("1.0", tk.END).strip(),
                "abdomen": self.abdomen_text.get("1.0", tk.END).strip(),
                "musculoskeletal": self.msk_text.get("1.0", tk.END).strip(),
                "neurological": self.neuro_text.get("1.0", tk.END).strip()
            },
            "diagnostic_tests": {
                "lab_tests": self.lab_tests,
                "imaging_studies": self.imaging_studies,
                "biopsies": self.biopsies,
                "ecg_results": self.ecg_results,
                "other_tests": self.other_tests
            },
            "notes": self.notes_text.get("1.0", tk.END).strip(),
            "date_created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        filename = f"{self.name_var.get().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            initialfile=filename,
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Save Medical Record"
        )
        
        if file_path:
            try:
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                with open(file_path, 'w') as f:
                    json.dump(record, f, indent=4)
                
                messagebox.showinfo("Success", "Medical record saved successfully!")
                self.clear_form()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save record: {str(e)}")
        else:
            messagebox.showinfo("Cancelled", "Save operation cancelled.")
    
    def clear_form(self):
        self.name_var.set("")
        self.dob_calendar.set_date(datetime.now())
        self.gender_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.emergency_name_var.set("")
        self.emergency_phone_var.set("")
        self.emergency_relation_var.set("")
        self.insurance_provider_var.set("")
        self.policy_number_var.set("")
        self.bp_systolic_var.set("")
        self.bp_diastolic_var.set("")
        self.heart_rate_var.set("")
        self.respiratory_rate_var.set("")
        self.temperature_var.set("")
        self.height_var.set("")
        self.weight_var.set("")
        self.bmi_var.set("")
        self.bmi_category_var.set("")
        self.bmi_category_combo.set("")
        
        self.chronic_conditions_text.delete("1.0", tk.END)
        self.surgeries_text.delete("1.0", tk.END)
        self.hospitalizations_text.delete("1.0", tk.END)
        self.family_history_text.delete("1.0", tk.END)
        self.smoking_var.set("")
        self.alcohol_var.set("")
        self.drug_var.set("")
        self.occupation_var.set("")
        self.lifestyle_text.delete("1.0", tk.END)
        self.immunization_text.delete("1.0", tk.END)
        self.allergies_text.delete("1.0", tk.END)
        self.medications_text.delete("1.0", tk.END)
        self.coverage_text.delete("1.0", tk.END)
        self.notes_text.delete("1.0", tk.END)
        
        self.heart_rate_var.set("")
        self.hr_status_var.set("")
        self.draw_heart_rate_range()  
        
        self.height_var.set("")
        self.weight_var.set("")
        self.bmi_var.set("")
        self.bmi_category_var.set("")
        self.bmi_category_combo.set("")
        self.draw_bmi_range()  
        
        
        self.general_appearance_text.delete("1.0", tk.END)
        self.head_text.delete("1.0", tk.END)
        self.eyes_text.delete("1.0", tk.END)
        self.ears_text.delete("1.0", tk.END)
        self.nose_text.delete("1.0", tk.END)
        self.throat_text.delete("1.0", tk.END)
        self.cv_text.delete("1.0", tk.END)
        self.resp_text.delete("1.0", tk.END)
        self.abdomen_text.delete("1.0", tk.END)
        self.msk_text.delete("1.0", tk.END)
        self.neuro_text.delete("1.0", tk.END)
        
        
        self.lab_tests = []
        self.imaging_studies = []
        self.biopsies = []
        self.ecg_results = []
        self.other_tests = []
        
        
        self.clear_lab_test_fields()
        self.clear_imaging_fields()
        self.clear_biopsy_fields()
        self.clear_ecg_fields()
        self.clear_other_test_fields()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleMedicalRecord(root)
    root.mainloop() 
