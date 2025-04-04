# -*- coding: utf-8 -*-
{
    'name': "Education Management",

    'summary': "Education Management System for High School",

    'description': """
    Education Management System for High School
    """,

    'author': "Muhammad Ridho Ramadhan",
    'website': "https://www.yourcompany.com",

    'category': 'Education',
    'version': '0.1',

    'depends': ['base', 'mail', 'l10n_id_efaktur','web', 'sale'],
    
    'assets': {
        'web.assets_backend': [
            'education_management/static/src/css/style.css',
        ],
    },

    'data': [
        'data/education_student_sequence.xml',
        'data/education_classroom_sequence.xml',
        'data/education_major_sequence.xml',
        'data/education_subject_sequence.xml',
        'data/ir_cron_data.xml',
        'report/education_student_id_card.xml',
        'report/education_teacher_id_card.xml',
        'report/assessment_student_report.xml',
        'report/teacher_evaluation_report.xml',
        'report/student_attendance_report.xml',
        'security/ir.model.access.csv', 
        'views/education_student_views.xml',
        'wizard/student_attendance_wizard_views.xml',
        'views/education_classroom_views.xml',
        'views/education_major_views.xml',
        'views/res_partner_views.xml',
        'views/education_subject_views.xml',
        'views/student_attendance_views.xml',
        'views/education_student_menu_views.xml',
    ],
    
    'images': ['education_management/static/description/icon.png'],
    
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'installable': True,
}

