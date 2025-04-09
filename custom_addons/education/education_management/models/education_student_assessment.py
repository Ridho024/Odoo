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
    
    @api.constrains('assessment_id')
    def _check_total_weight(self):
        for record in self:
            if record.assessment_id:
                total = sum(record.assessment_id.assessment_criteria_ids.mapped('weight'))
                if total > 100:
                    raise ValidationError("Total weight of all criteria for this assessment cannot exceed 100%.")
    
class StudentAssessmentResult(models.Model):
    _name = 'student.assessment.result'
    _description = 'Student Assessment Result'
    
    assessment_id = fields.Many2one('education.student.assessment', string='Assessment Record', readonly=True)
    student_id = fields.Many2one('education.student', string='Student', ondelete='cascade')
    correct_answer = fields.Integer(string='Correct Answer', required=True)
    score = fields.Float(string='Total Score (%)', compute='_calculate_total_score')
    
    @api.depends('correct_answer', 'assessment_id.total_question')
    def _calculate_total_score(self):
        for result in self:
            total_question = result.assessment_id.total_question
            result.score = (result.correct_answer / total_question) * 100 if total_question else 0.0

                