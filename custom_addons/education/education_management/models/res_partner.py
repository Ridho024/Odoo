from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import random, string

class ResPartner(models.Model):
    _inherit ='res.partner'
    
    is_teacher = fields.Boolean(string='Is Teacher')
    gender = fields.Selection([('male', 'Male'),
                               ('female', 'Female')
                               ], string='Gender')
    
    # Education Management
    major_ids = fields.Many2many('education.major', string='Major Assigned')
    subject_ids = fields.Many2many('education.subject', string='Subject Taught')
    
    # Administration
    nip = fields.Char(string='NIP')
    
    # Teacher Authentication
    teacher_login_id = fields.Many2one('res.users', string='Related User', readonly=True)
    
    def action_create_teacher_user(self):
        """Membuat user Odoo dari partner jika is_teacher = True"""
        self.ensure_one()
        for partner in self:
            if not partner.teacher_login_id and partner.is_teacher:
                if not self.email:
                    raise ValidationError(_("Teacher must have an email to create a user."))
                
                # Generate password random
                password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                
                user_vals = {
                    'name': partner.name,
                    'login': partner.email,
                    'partner_id': partner.id,
                    'groups_id': [(6, 0, [self.env.ref('base.group_user').id])],
                    'password': password,
                }
                
                new_user = self.env['res.users'].create(user_vals)
                partner.teacher_login_id = new_user.id
                
                # Opsional: Menampilkan password ke user (bisa disimpan di log atau dikirim ke email)
                message_id = self.env['message.wizard'].create({'message': _(f'User berhasil dibuat!\nLogin: {new_user.login}\nPassword: {password}')})
                
                return {
                    'name': _('Successfull Creating User'),
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'message.wizard',
                    # pass the id
                    'res_id': message_id.id,
                    'target': 'new'
                }
            else:
                raise ValidationError(_("User login for this id is already exist."))
            
    def action_create_teacher_card(self):
        return (self.env.ref('education_management.action_teacher_id_card_report').report_action(self))
    
    def action_create_attendance(self):
        """This function is called when the user clicks the
            'Create Attendance' button on a student's list view. It opens a
            new wizard to compose and create and attendance message."""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Teacher Attendance'),
            'res_model': 'wizard.teacher.attendance',
            'target': 'new',
            'view_mode': 'form',
            'view_type': 'form',
            'context': {
                'default_teacher_id': self.id,
                },
        }