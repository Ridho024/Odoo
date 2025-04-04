from odoo import models, fields, api

class AssessmentResult(models.Model):
    _name = 'assessment.result'
    _description = 'Student Assessment Result'
    
    assessment_id = fields.Many2one('assessment.record', string='Assessment Record', readonly=True)
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