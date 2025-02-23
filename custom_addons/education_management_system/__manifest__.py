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
        'education_class_views.xml',
        'education_teacher_views.xml',
        'education_student_views.xml',
        'education_management_system_menu.xml',
    ],
    
    'demo': [
        'demo/demo.xml',
    ],
    
    'application': True,
    'installable': True,
}

