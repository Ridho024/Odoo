from odoo import models, fields

class TeacherFeedback(models.Model):
    _name = 'teacher.feedback'
    _description = 'Teacher Feedback'  
    
    evaluation_id = fields.Many2one("teacher.evaluation", string="Evaluasi", required=True, ondelete="cascade")
    feedback_text = fields.Text(string="Feedback")
    improvement_text = fields.Text(string="Improvement")