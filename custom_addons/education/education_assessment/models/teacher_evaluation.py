from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TeacherEvaluation(models.Model):
    _name = 'teacher.evaluation'
    _description = 'Teacher Evaluation'
    
    name = fields.Char(string='Evaluation Name', required=True)
    teacher_id = fields.Many2one('res.partner', string='Teacher')
    evaluator_id = fields.Many2one('res.users', string='Evaluator', required=True, help='Teacher evaluator')
    date = fields.Date(string='Date', default=fields.Date.today())
    evaluation_result_ids = fields.One2many('teacher.evaluation.result', 'evaluation_id', string='Evaluation Result')
    feedback_ids = fields.One2many('teacher.feedback', 'evaluation_id', string='Feedback')
    total_score = fields.Float(string='Total Score')

    @api.constrains("total_score")
    def _check_total_score(self):
        for record in self:
            if record.total_score < 0 or record.total_score > 100:
                raise ValidationError("Total nilai harus berada di antara 0 dan 100.")
