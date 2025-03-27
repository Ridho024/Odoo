from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TeacherEvaluationResult(models.Model):
    _name = 'teacher.evaluation.result'
    _description = 'Teacher Evaluation Result'
    
    evaluation_id = fields.Many2one('teacher.evaluation', string='Evaluation', ondelete='cascade', readonly=True)
    criteria_id = fields.Many2one('teacher.evaluation.criteria', string='Evaluation Criteria', required=True)
    score = fields.Float(string='Score')
    
    @api.constrains("score")
    def _check_score(self):
        for record in self:
            if record.score < 0 or record.score > 100:
                raise ValidationError("Nilai harus berada di antara 0 dan 100.")