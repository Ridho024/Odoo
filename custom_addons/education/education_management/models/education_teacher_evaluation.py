from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TeacherEvaluation(models.Model):
    _name = 'education.teacher.evaluation'
    _description = 'Teacher Evaluation'
    
    name = fields.Char(string='Evaluation Name', required=True)
    teacher_id = fields.Many2one('res.partner', string='Teacher', domain=[('is_teacher', '=', True)], required=True, help='Teacher to be evaluated')
    evaluator_id = fields.Many2one('res.users', string='Evaluator', required=True, help='Teacher evaluator')
    date = fields.Date(string='Date', default=fields.Date.today(), required=True)
    evaluation_result_ids = fields.One2many('teacher.evaluation.result', 'evaluation_id', string='Evaluation Result')
    feedback_ids = fields.One2many('teacher.evaluation.feedback', 'evaluation_id', string='Feedback')
    total_score = fields.Float(string='Total Score', compute='_compute_total_score', store=True)

    @api.depends('evaluation_result_ids.score')
    def _compute_total_score(self):
        for record in self:
            scores = [result.score for result in record.evaluation_result_ids if result.score is not None]
            record.total_score = sum(scores) / len(scores) if scores else 0.0
            
class TeacherEvaluationCriteria(models.Model):
    _name = 'teacher.evaluation.criteria'
    _description = 'Teacher Evaluation Criteria'
    
    name = fields.Char(string='Criteria Name', required=True)
    weight = fields.Float(string='Weight (%)', help='Criteria weight in persen.')
    

class TeacherEvaluationResult(models.Model):
    _name = 'teacher.evaluation.result'
    _description = 'Teacher Evaluation Result'
    
    evaluation_id = fields.Many2one('education.teacher.evaluation', string='Evaluation', ondelete='cascade', readonly=True)
    criteria_id = fields.Many2one('teacher.evaluation.criteria', string='Evaluation Criteria', required=True)
    score = fields.Float(string='Score')
    
    @api.constrains("score")
    def _check_score(self):
        for record in self:
            if record.score < 0 or record.score > 100:
                raise ValidationError("Nilai harus berada di antara 0 dan 100.")
            
class TeacherFeedback(models.Model):
    _name = 'teacher.evaluation.feedback'
    _description = 'Teacher Feedback'  
    
    evaluation_id = fields.Many2one("education.teacher.evaluation", string="Evaluasi", required=True, ondelete="cascade")
    feedback_text = fields.Text(string="Feedback")
    improvement_text = fields.Text(string="Improvement")