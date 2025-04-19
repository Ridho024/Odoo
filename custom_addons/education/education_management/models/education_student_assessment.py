from odoo import models, fields, api
from odoo.exceptions import ValidationError


class EducationStudentAssessment(models.Model):
    _name = 'education.student.assessment'
    _description = 'Student Assessment Record'
    _rec_name = 'subject_id'
    _order = 'date asc'

    subject_id = fields.Many2one('education.subject', string='Subject', required=True)
    category = fields.Selection([
        ('daily_task', 'Daily Task'),
        ('daily_exam', 'Daily Exam'),
        ('midterm_exam', 'Midterm Exam'),
        ('final_exam', 'Final Exam'),
        ('practical_exam', 'Practical Exam')
    ], string='Category', required=True)

    semester = fields.Selection([
        ('1', 'Semester 1'),
        ('2', 'Semester 2')
    ], string='Semester', required=True)

    classroom_id = fields.Many2one('education.classroom', string='Classroom', required=True)
    teacher_id = fields.Many2one('res.partner', string='Teacher', domain="[('is_teacher', '=', True)]")
    date = fields.Date(string='Date', default=fields.Date.context_today, required=True)
    assessment_file = fields.Binary(string='Assessment File', required=True)
    total_question = fields.Integer(string='Total Questions', required=True)
    passing_score = fields.Float(string='Passing Score (%)', default=70.0, help='Minimum score to pass the assessment')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done')
    ], string='Status', default='draft')

    assessment_criteria_ids = fields.One2many(
        'student.assessment.criteria', 'assessment_id', string='Assessment Criteria'
    )
    assessment_result_ids = fields.One2many(
        'student.assessment.result', 'assessment_id', string='Assessment Results'
    )

    def action_confirm(self):
        for rec in self:
            rec.state = 'done'

    def action_reset(self):
        for rec in self:
            rec.state = 'draft'


class StudentAssessmentCriteria(models.Model):
    _name = 'student.assessment.criteria'
    _description = 'Assessment Criteria'

    name = fields.Char(string='Name', required=True)
    weight = fields.Float(string='Weight (%)')
    assessment_id = fields.Many2one(
        'education.student.assessment', string='Assessment Record',
        ondelete='cascade', required=True
    )

    @api.constrains('weight', 'assessment_id')
    def _check_total_weight(self):
        for record in self:
            if record.assessment_id:
                total = sum(record.assessment_id.assessment_criteria_ids.mapped('weight'))
                if total > 100:
                    raise ValidationError("Total weight of all criteria cannot exceed 100%.")


class StudentAssessmentResult(models.Model):
    _name = 'student.assessment.result'
    _description = 'Student Assessment Result'

    assessment_id = fields.Many2one(
        'education.student.assessment', string='Assessment Record',
        required=True, ondelete='cascade', readonly=True
    )
    student_id = fields.Many2one(
        'education.student', string='Student',
        required=True, ondelete='cascade'
    )
    correct_answer = fields.Integer(
        string='Correct Answers', required=True,
        help='Number of correct answers by the student.'
    )
    score = fields.Float(
        string='Total Score (%)', compute='_compute_score', store=True,
        help='Score based on correct answers and total questions.'
    )
    is_passed = fields.Boolean(
        string='Passed?', compute='_compute_passed', store=True,
        help='Automatically set if the student passed.'
    )

    @api.depends('correct_answer', 'assessment_id.total_question')
    def _compute_score(self):
        for result in self:
            total = result.assessment_id.total_question
            result.score = (result.correct_answer / total) * 100 if total else 0.0

    @api.depends('score', 'assessment_id.passing_score')
    def _compute_passed(self):
        for rec in self:
            rec.is_passed = rec.score >= rec.assessment_id.passing_score

    @api.constrains('score')
    def _check_score_limits(self):
        for result in self:
            if result.score < 0 or result.score > 100:
                raise ValidationError("Score must be between 0 and 100.")
