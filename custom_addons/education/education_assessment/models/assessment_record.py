from odoo import models, fields

class AssessmentRecord(models.Model):
    _name = 'assessment.record'
    _description = 'Student Assessment Record'
    _rec_name = 'subject_id'
    
    subject_id = fields.Many2one('education.subject', string='Subject')
    category = fields.Selection([('daily_task', 'Daily Task'),
                                   ('daily_exam', 'Daily Exam'),
                                   ('midterm_exam', 'Midterm Exam'),
                                   ('final_exam', 'Final Exam'),
                                   ('practical_exam', 'Practical Exam')], string='Category')
    semester = fields.Selection([('1', 'Semester 1'),
                                 ('2', 'Semester 2')], string='Semester')
    classroom_id = fields.Many2one('education.classroom', string='Classroom')
    teacher_id = fields.Many2one('res.partner', string='Teacher', domain=[('is_teacher', '=', True)], help='Teacher who give the assessment or supervisor')
    date = fields.Date(string='Date', default= fields.Date.today())
    assessment_file = fields.Binary(string='Assessment File')
    total_question = fields.Integer(string='Total Question')
    assessment_criteria_ids = fields.One2many('assessment.criteria', 'assessment_id', string='Assessment Criteria')
    assessment_result_ids = fields.One2many('assessment.result', 'assessment_id', string='Assessment Results')
    student_ids = fields.Many2many('education.student', string='Students', related='classroom_id.student_ids', readonly=True, help='List of student in the classroom choosed')