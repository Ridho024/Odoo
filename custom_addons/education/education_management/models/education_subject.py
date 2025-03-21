from odoo import models, fields

class EducationSubject(models.Model):
    _name = 'education.subject'
    _description = 'Education Subject'
    
    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True, copy=True, readonly=True, default=lambda self: self.env['ir.sequence'].next_by_code('education.subject') or 'New')
    teacher_id = fields.Many2one('res.partner', string='Instructor', required=True, help='Instructor for this subject', domain="[('is_teacher', '=', True)]")
    teacher_ids = fields.Many2many('res.partner', string='Teachers', help='List teachers for this subject', domain="[('is_teacher', '=', True)]")
    subject_ids = fields.One2many('education.subject.detail', 'subject_id', string='Subject Details', help='Subject Details')