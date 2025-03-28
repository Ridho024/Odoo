from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AssessmentResult(models.Model):
    _name = 'assessment.result'
    _description = 'Student Assessment Result'
    
    assessment_id = fields.Many2one('assessment.record', string='Assessment Record', readonly=True)
    total_question = fields.Integer(string='Total Question', related='assessment_id.total_question', readonly=True)
    student_id = fields.Many2one('education.student', string='Student', required=True, domain="[('id', 'in', student_ids)]")
    correct_answer = fields.Integer(string='Correct Answer', required=True)
    incorrect_answer = fields.Integer(string='Incorrect Answer', required=True)
    score = fields.Float(string='Total Score (%)', compute='_calculate_total_score')
    student_ids = fields.Many2many('education.student', string='Students', compute='_compute_students', store=False)
    
    @api.depends('correct_answer', 'incorrect_answer')
    def _calculate_total_score(self):
        for result in self:
            if result.correct_answer and result.total_question:
                total_score = (result.correct_answer / result.total_question) * 100
                result.score = total_score
            else:
                result.score = 0.00
                
    @api.depends('assessment_id')
    def _compute_students(self):
        for record in self:
            record.student_ids = record.assessment_id.student_ids if record.assessment_id else False


    # @api.constrains("score")
    # def _check_score(self):
    #     for record in self:
    #         if record.score < 0 or record.score > 100:
    #             raise ValidationError("Nilai harus berada di antara 0 dan 100.")
    
"""
LIST TO DO:
- Create system untuk absensi penilaian siswa dan guru.
"""
