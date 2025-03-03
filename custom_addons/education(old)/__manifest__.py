# -*- coding: utf-8 -*-
{
    'name': "Online Course Managemesnt System",

    'summary': "Online course management system for web-based education.",

    'description': """
    Fitur utama:
        - Manajemen siswa, guru, dan kelas.
        - Jadwal pelajaran.
        - Manajemen ujian & nilai.
        - Pembayaran biaya pendidikan.
    """,
    
    'author': "Muhammad Ridho Ramadhan",
    
    'website': "https://github.com/Ridho024",
    
    'category': 'Education',
    
    'version': '0.1',
    
    'depends': ['base', 'calendar'],
    
    'assets': {
        'web.assets_backend': [
            'education/static/src/css/style.css',
        ],
    },
    
    'data': [
        'views/student_class_views.xml',
        'views/teacher_teacher_views.xml',
        'views/teacher_employement_views.xml',
        'views/student_student_views.xml',
        'views/student_department_views.xml',
        'views/classroom_views.xml',
        'views/education_management_system_menu.xml',
        'security/ir.model.access.csv',
    ],
    
    'demo': [
        'demo/demo.xml',
    ],
    
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}

