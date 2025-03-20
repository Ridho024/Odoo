from odoo import models, fields

class EducationMajor(models.Model):
    _name = 'education.major'
    _description = 'Education Major'
    
    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True, copy=True, readonly=True, default=lambda self: self.env['ir.sequence'].next_by_code('education.major') or 'New')
    teacher_id = fields.Many2one('education.teacher', string='Instructor', required=True, help="Main instructor for this course")
    teacher_ids = fields.Many2many('education.teacher', string='Teachers', help='List teachers for this major')
    curriculum_ids = fields.One2many('education.major.curriculum', 'major_id', string='Curriculum', help='Curriculum Details')
    academic_year = fields.Char(string='Academic Year', help='Academic year for this major')
    color = fields.Integer(string='Color', readonly=True)