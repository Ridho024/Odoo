from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import random, string

class ResPartner(models.Model):
    _inherit ='res.partner'
    
    is_teacher = fields.Boolean(string='Is Teacher')
    gender = fields.Selection([('male', 'Male'),
                               ('female', 'Female')
                               ], string='Gender')
    # subject_ids = fields.Many2many('education.subject', string='Subjects')
    class_ids = fields.Many2many('education.classroom', string='Assigned Classes')
    
    # Education Management
    major_ids = fields.Many2many('education.major', string='Major Assigned')
    class_ids = fields.Many2many('education.classroom', string='Class Assigned')
    
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
    
class WizardTeacherAttendance(models.TransientModel):
    _name = 'wizard.teacher.attendance'
    _description = 'Wizard Teacher Attendance'
    
    teacher_id = fields.Many2one('res.partner', string='Teacher')
    classroom_id = fields.Many2one('education.classroom', string='Classroom')
    date = fields.Date(string='Date', default=fields.Date.today())
    subject_id = fields.Many2one('education.subject', string='Subject')
    status = fields.Selection([('present', 'Present'),
                               ('absent', 'Absent')], string='Status', default='absent')
    absent_reason = fields.Selection([('permit', 'Izin'),
                                      ('sick', 'Sick'),
                                      ('alpha', 'Alpha')], string='Absent Reason', default='permit')
    
    @api.model
    def create(self, vals):
        res = super(WizardTeacherAttendance, self).create(vals)
        
        attendance = {
            'teacher_id': res.teacher_id,
            'classroom_id': res.classroom_id,
            'date': res.date,
            'subject_id': res.subject_id,
            'status': res.status,
            'absent_reason': res.absent_reason,
        }
        
        self.env['education.teacher.attendance'].create(attendance)
        
        return res