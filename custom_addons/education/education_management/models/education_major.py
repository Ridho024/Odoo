from odoo import models, fields, api, _

class EducationMajor(models.Model):
    _name = 'education.major'
    _description = 'Education Major'
    _sql_constraints = [
        ('name', 'unique(name)', 'Major with this name already exists!'),
    ]
    
    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True, copy=False, readonly=True, index=True, default='New')
    teacher_id = fields.Many2one('res.partner', string='Instructor', required=True, help="Main instructor for this major", domain="[('is_teacher', '=', True)]")
    teacher_ids = fields.Many2many('res.partner', string='Teachers', help='List teachers for this major', domain="[('is_teacher', '=', True)]")
    curriculum_ids = fields.One2many('education.major.curriculum', 'major_id', string='Curriculum', help='Curriculum Details')
    academic_year = fields.Char(string='Academic Year', required=True, help='Academic year for this major')
    color = fields.Integer(string='Color', readonly=True)
    
    @api.model_create_multi
    def create(self,vals_list):
        """ Create a sequence for the education major model """
        """Optimized create method for education major"""
        # Update only records that need an ID
        for vals in vals_list:
            if vals.get('code', _('New')) == _('New'):
                vals['code'] = self.env['ir.sequence'].next_by_code('education.major')

        # Call super to create records
        return super(EducationMajor, self).create(vals_list)
