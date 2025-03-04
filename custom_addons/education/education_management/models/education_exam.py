from odoo import models, fields, api

class EducationExam(models.Model):
    _name ='education.exam'
    _description = 'Student Exams'
    
    name = fields.Char(string='Exam Name', required=True)
    description = fields.Text(string='Description')
    course_id = fields.Many2one('education.course', string='Course', required=True)
    classroom_id = fields.Many2one('education.classroom', string='Classroom')
    exam_date = fields.Date(string='Exam Date', required=True)
    duration = fields.Integer(string="Duration (Minutes)", default=60)
    exam_type = fields.Selection([
        ('offline', 'Offline'),
        ('online', 'Online'),
    ], string='Exam Type', default='offline')
    student_ids = fields.Many2many('education.student', string='Participants')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('graded', 'Graded'),
    ], string='Status', default='draft')
    exam_results_ids = fields.One2many('education.exam.result', 'exam_id', string='Exam Results')
    
    # Metode untuk Menjadwalkan Ujian
    def action_schedule(self):
        self.write({'state': 'scheduled'})

    # Metode untuk Menandai Ujian sebagai Selesai
    def action_complete(self):
        self.write({'state': 'completed'})

    # Metode untuk Menandai Ujian sebagai Dinilai
    def action_grade(self):
        self.write({'state': 'graded'})
