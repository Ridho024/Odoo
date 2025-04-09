from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TeacherEvaluation(models.Model):
    _name = 'education.teacher.evaluation'
    _description = 'Teacher Evaluation'
    _order = 'date desc, name'

    name = fields.Char(string='Evaluation Name', required=True)
    teacher_id = fields.Many2one(
        'res.partner', string='Teacher', required=True,
        domain=[('is_teacher', '=', True)],
        help='Teacher to be evaluated'
    )
    evaluator_id = fields.Many2one(
        'res.users', string='Evaluator', required=True,
        help='User who evaluates the teacher'
    )
    date = fields.Date(string='Evaluation Date', default=fields.Date.today, required=True)

    evaluation_result_ids = fields.One2many(
        'teacher.evaluation.result', 'evaluation_id',
        string='Evaluation Results'
    )
    feedback_ids = fields.One2many(
        'teacher.evaluation.feedback', 'evaluation_id',
        string='Feedbacks'
    )

    total_score = fields.Float(
        string='Total Score',
        compute='_compute_total_score',
        store=True,
        readonly=True
    )

    @api.depends('evaluation_result_ids.score')
    def _compute_total_score(self):
        for record in self:
            scores = [line.score for line in record.evaluation_result_ids if line.score is not None]
            record.total_score = sum(scores) / len(scores) if scores else 0.0
            
class TeacherEvaluationCriteria(models.Model):
    _name = 'teacher.evaluation.criteria'
    _description = 'Teacher Evaluation Criteria'
    _order = 'name'

    name = fields.Char(string='Criteria Name', required=True)
    weight = fields.Float(string='Weight (%)', help='Percentage weight of this criteria')   

class TeacherEvaluationResult(models.Model):
    _name = 'teacher.evaluation.result'
    _description = 'Teacher Evaluation Result'
    _rec_name = 'criteria_id'

    evaluation_id = fields.Many2one(
        'education.teacher.evaluation', string='Evaluation',
        ondelete='cascade', required=True
    )
    criteria_id = fields.Many2one(
        'teacher.evaluation.criteria', string='Criteria',
        required=True
    )
    score = fields.Float(string='Score')

    @api.constrains('score')
    def _check_score_range(self):
        for record in self:
            if not (0 <= record.score <= 100):
                raise ValidationError("Score must be between 0 and 100.")
            
class TeacherFeedback(models.Model):
    _name = 'teacher.evaluation.feedback'
    _description = 'Teacher Feedback'
    _rec_name = 'feedback_text'

    evaluation_id = fields.Many2one(
        'education.teacher.evaluation', string='Evaluation',
        ondelete='cascade', required=True
    )
    feedback_text = fields.Text(string='Feedback')
    improvement_text = fields.Text(string='Suggested Improvements')
