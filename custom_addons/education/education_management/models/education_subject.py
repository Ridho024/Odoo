from odoo import models, fields, api, _

class EducationSubject(models.Model):
    _name = 'education.subject'
    _description = 'Education Subject'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True, copy=False, readonly=True, default='New')
    teacher_id = fields.Many2one(
        'res.partner', string='Instructor', required=True,
        domain="[('is_teacher', '=', True)]", help='Main instructor for this subject'
    )
    teacher_ids = fields.Many2many(
        'res.partner', string='Additional Teachers',
        domain="[('is_teacher', '=', True)]", help='List of supporting teachers'
    )
    subject_ids = fields.One2many(
        'education.subject.detail', 'subject_id',
        string='Subject Details', help='Curriculum-based subject contents'
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('code', _('New')) == _('New'):
                vals['code'] = self.env['ir.sequence'].next_by_code('education.subject') or _('New')
        return super().create(vals_list)
