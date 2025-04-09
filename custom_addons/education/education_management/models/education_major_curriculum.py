from odoo import models, fields

class EducationMajorCurriculum(models.Model):
    _name = 'education.major.curriculum'
    _description = 'Education Major Curriculum'
    _rec_name = 'major_id'
    
    major_id = fields.Many2one('education.major', string='Major', readonly=True)
    core_competency = fields.Text(string='Core Competency')
    basic_competency = fields.Text(string='Basic Competency')
    