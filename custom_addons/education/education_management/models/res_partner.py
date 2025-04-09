from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import random
import string

class ResPartner(models.Model):
    _inherit = 'res.partner'

    _sql_constraints = [
        ('nip_unique', 'unique(nip)', 'NIP number must be unique for all teachers!'),
    ]

    # Teacher Info
    is_teacher = fields.Boolean(string='Is Teacher')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender')
    nip = fields.Char(string='NIP')
    teacher_login_id = fields.Many2one('res.users', string='Related User', readonly=True)

    # Education Management
    major_ids = fields.Many2many('education.major', string='Majors Assigned')
    subject_ids = fields.Many2many('education.subject', string='Subjects Taught')

    def action_create_teacher_user(self):
        """Create related user account for a teacher."""
        self.ensure_one()
        
        if self.teacher_login_id:
            raise ValidationError(_("User login for this teacher already exists."))

        if not self.is_teacher:
            raise ValidationError(_("This contact is not marked as a teacher."))

        if not self.email:
            raise ValidationError(_("Teacher must have an email to create a user."))

        # Generate random password
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        user_vals = {
            'name': self.name,
            'login': self.email,
            'partner_id': self.id,
            'groups_id': [(6, 0, [self.env.ref('base.group_user').id])],
            'password': password,
        }

        new_user = self.env['res.users'].create(user_vals)
        self.teacher_login_id = new_user

        # Optional: Show message with login details
        message = _(
            'User successfully created!\n\n'
            'Login: {}\nPassword: {}'
        ).format(new_user.login, password)

        message_id = self.env['message.wizard'].create({'message': message})
        return {
            'name': _('User Created'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'message.wizard',
            'res_id': message_id.id,
            'target': 'new'
        }
