from odoo import models, fields, api, _

class EducationSubject(models.Model):
    _name = 'education.subject'
    _description = 'Education Subject'
    
    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True, copy=True, readonly=True, default='New')
    teacher_id = fields.Many2one('res.partner', string='Instructor', required=True, help='Instructor for this subject', domain="[('is_teacher', '=', True)]")
    teacher_ids = fields.Many2many('res.partner', string='Teachers', help='List teachers for this subject', domain="[('is_teacher', '=', True)]")
    subject_ids = fields.One2many('education.subject.detail', 'subject_id', string='Subject Details', help='Subject Details')
    
    @api.model_create_multi
    def create(self,vals_list):
        """ Create a sequence for the education subject model """
        """Optimized create method for education subject"""
        # Update only records that need an ID
        for vals in vals_list:
            if vals.get('code', _('New')) == _('New'):
                vals['code'] = self.env['ir.sequence'].next_by_code('education.subject')

        # Call super to create records
        return super(EducationSubject, self).create(vals_list)