# -*- coding: utf-8 -*-
{
    'name': "Student & Teacher Assessment",

    'summary': "Education Management second module for Student & Teacher Assessment",

    'description': """
        Student:
        - Daily Assessment
        - Exam
        - Midterm Test
        - Final Semester Test
        Teacher:
        - Teacher evaluation metrics
        
        "There are no stupid students, they just haven't met the right teacher yet." - Anonimus 2025.
    """,

    'author': "Ridho024",
    'website': "https://github.com/Ridho024",

    'category': 'Education',
    'version': '0.1',
    
    'web.assets_backend': [
        'education_assessment/static/src/css/style.css',
    ],

    'depends': ['base'],

    'data': [
        'report/assessment_record_report.xml',
        'security/ir.model.access.csv',
        'views/assessment_record_views.xml',
        'views/teacher_evaluation_views.xml',
    ],

    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
}

