from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AssessmentResult(models.Model):
    _name = 'assessment.result'
    _description = 'Student Assessment Result'
    
    assessment_id = fields.Many2one('assessment.record', string='Assessment Record')
    student_id = fields.Many2one('education.student', string='Student')
    score = fields.Float(string='Score')
    remarks = fields.Text(string='Remarks')
    
    @api.constrains("score")
    def _check_score(self):
        for record in self:
            if record.score < 0 or record.score > 100:
                raise ValidationError("Nilai harus berada di antara 0 dan 100.")
