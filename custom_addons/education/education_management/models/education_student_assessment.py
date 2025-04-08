from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EducationStudentAssessment(models.Model):
    _name = 'education.student.assessment'
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
    assessment_criteria_ids = fields.One2many('student.assessment.criteria', 'assessment_id', string='Assessment Criteria')
    assessment_result_ids = fields.One2many('student.assessment.result', 'assessment_id', string='Assessment Results')
    
class StudentAssessmentCriteria(models.Model):
    _name = 'student.assessment.criteria'
    _description = 'Assessment Criteria'
    
    name = fields.Char(string='Name', required=True)
    weight = fields.Float(string='Weight (%)')
    assessment_id = fields.Many2one('education.student.assessment', string='Assessment Record')
    
    @api.depends('weight')
    def _compute_maximum_weight(self):
        for record in self:
            total_weight = sum(record.mapped('weight'))
            if total_weight > 100:
                raise ValidationError("Total weight cannot exceed 100%.")
    
class StudentAssessmentResult(models.Model):
    _name = 'student.assessment.result'
    _description = 'Student Assessment Result'
    
    assessment_id = fields.Many2one('education.student.assessment', string='Assessment Record', readonly=True)
    student_id = fields.Many2one('education.student', string='Student', ondelete='cascade')
    correct_answer = fields.Integer(string='Correct Answer', required=True)
    score = fields.Float(string='Total Score (%)', compute='_calculate_total_score')
        
    # For report
    semester = fields.Selection([('1', 'Semester 1'),
                                 ('2', 'Semester 2')], string='Semester', compute='_compute_assessment_fields', store=True)
    category = fields.Selection([('daily_task', 'Daily Task'),
                                   ('daily_exam', 'Daily Exam'),
                                   ('midterm_exam', 'Midterm Exam'),
                                   ('final_exam', 'Final Exam'),
                                   ('practical_exam', 'Practical Exam')], string='Category', compute='_compute_assessment_fields', store=True)
    subject_id = fields.Many2one('education.subject', string='Subject', compute="_compute_assessment_fields", store=True)
    
    @api.depends('assessment_id')
    def _compute_assessment_fields(self):
        for record in self:
            record.semester = record.assessment_id.semester if record.assessment_id else False
            record.category = record.assessment_id.category if record.assessment_id else False
            record.subject_id = record.assessment_id.subject_id.id if record.assessment_id else False
    
    @api.depends('correct_answer')
    def _calculate_total_score(self):
        for result in self:
            total_question = result.assessment_id.total_question
            if result.correct_answer and total_question:
                total_score = (result.correct_answer / total_question) * 100
                result.score = total_score
            else:
                result.score = 0.00
                