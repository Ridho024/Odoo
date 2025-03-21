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

    'depends': ['base', 'mail', 'l10n_id_efaktur'],
    
    'assets': {
        'web.assets_backend': [
            'education_management/static/src/css/style.css',
        ],
    },

    'data': [
        'data/education_student_sequence.xml',
        'data/education_classroom_sequence.xml',
        'data/education_major_sequence.xml',
        'security/ir.model.access.csv',
        'views/education_student_views.xml',
        'views/education_student_attendance_views.xml',
        'views/education_teacher_views.xml',
        'views/education_teacher_schedule_views.xml',
        'views/education_teacher_attendance_views.xml',
        'views/education_course_views.xml',
        'views/education_exam_views.xml',
        'views/education_classroom_views.xml',
        'views/education_course_category_views.xml',
        'views/education_major_views.xml',
        'views/res_partner_views.xml',
        'views/education_student_menu_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'installable': True,
}

