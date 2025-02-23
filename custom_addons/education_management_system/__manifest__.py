# -*- coding: utf-8 -*-
{
    'name': "Education Management System",

    'summary': "Education Management System (Manajemen Sekolah/Kursus)",

    'description': """
    Fitur utama:
        - Manajemen siswa, guru, dan kelas.
        - Jadwal pelajaran & absensi.
        - Manajemen ujian & nilai.
        - Pembayaran biaya pendidikan & faktur otomatis.
    """,
    
    'author': "Muhammad Ridho Ramadhan",
    
    'website': "https://github.com/Ridho024",
    
    'category': 'Manage',
    
    'version': '0.1',
    
    'depends': ['base'],
    
    'data': [
        'views/education_class_views.xml',
        'views/education_teacher_views.xml',
        'views/education_student_views.xml',
        'views/education_management_system_menu.xml',
        'security/ir.model.access.csv',
    ],
    
    'demo': [
        'demo/demo.xml',
    ],
    
    'application': True,
    'installable': True,
}

