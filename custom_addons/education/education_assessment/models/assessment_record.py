from odoo import models, fields

class AssessmentRecord(models.Model):
    _name = 'assessment.record'
    _description = 'Student Assessment Record'
    _rec_name = 'subject_id'
    _order = 'date asc'
    
    subject_id = fields.Many2one('education.subject', string='Subject', required=True, help='Subject of the assessment.')
    category = fields.Selection([('daily_task', 'Daily Task'),
                                   ('daily_exam', 'Daily Exam'),
                                   ('midterm_exam', 'Midterm Exam'),
                                   ('final_exam', 'Final Exam'),
                                   ('practical_exam', 'Practical Exam')], string='Category', required=True, help='Category for the assessment.')
    semester = fields.Selection([('1', 'Semester 1'),
                                 ('2', 'Semester 2')], string='Semester', required=True, help='Assessment semester 1 or 2')
    classroom_id = fields.Many2one('education.classroom', string='Classroom', required=True, help='Classroom for the assessment')
    teacher_id = fields.Many2one('res.partner', string='Teacher', help='Teacher who give the assessment or supervisor')
    date = fields.Date(string='Date', default= fields.Date.today(), required=True)
    assessment_file = fields.Binary(string='Assessment File', required=True, help='Assessment file in PDF format')
    total_question = fields.Integer(string='Total Question', required=True)
    assessment_criteria_ids = fields.One2many('assessment.criteria', 'assessment_id', string='Assessment Criteria')
    assessment_result_ids = fields.One2many('assessment.result', 'assessment_id', string='Assessment Results')