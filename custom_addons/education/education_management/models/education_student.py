from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class EducationStudent(models.Model):
    _name = 'education.student'
    _description = 'Education Student'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence'
    _sql_constraints = [
        ('nisn_unique', 'unique(nisn)', 'NISN must be unique!'),
        ('email_unique', 'unique(email)', 'Email must be unique or different from other student!'),
        ('phone_unique', 'unique(phone)', 'Phone number must be unique or different from other student!'),
        ('id_student_unique', 'unique(id_student)', 'Student ID must be unique!'),
        ('father_email_unique', 'unique(father_email)', 'Father email must be unique or different from other student!'),
        ('mother_email_unique', 'unique(mother_email)', 'Mother email must be unique or different from other student!'),
        ('father_contact_unique', 'unique(father_contact)', 'Father contact must be unique or different from other student!'),
        ('mother_contact_unique', 'unique(mother_contact)', 'Mother contact must be unique or different from other student!'),
    ]

    # === Basic Information ===
    sequence = fields.Integer(string='Sequence', default=10)
    name = fields.Char(string='Student Name', required=True, tracking=True, default="John Doe")
    nisn = fields.Char(string='NISN', required=True, tracking=True)
    id_student = fields.Char(
        string='Student ID',
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default='New',
        tracking=True
    )
    date_of_birth = fields.Date(string='Date of Birth', tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string='Gender', tracking=True)
    email = fields.Char(string='Student Email', tracking=True)
    phone = fields.Char(string='Student Phone', tracking=True)
    photo = fields.Image(string='Photo')

    # === Parent Information ===
    father_name = fields.Char(string='Father Name', tracking=True)
    father_contact = fields.Char(string='Father Contact', tracking=True)
    father_email = fields.Char(string='Father Email', tracking=True)
    mother_name = fields.Char(string='Mother Name', tracking=True)
    mother_contact = fields.Char(string='Mother Contact', tracking=True)
    mother_email = fields.Char(string='Mother Email', tracking=True)

    # === Academic Information ===
    classroom_id = fields.Many2one('education.classroom', string='Class', tracking=True, readonly=True)

    # === Student Status ===
    status = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('graduated', 'Graduated'),
        ('dropout', 'Dropout'),
    ], string='Status', tracking=True, compute='_compute_status', store=True)

    # === Achievements ===
    achievement_ids = fields.One2many(
        'education.student.achievement',
        'student_id',
        string='Academic Achievements',
        tracking=True
    )

    # === Computed Methods ===
    @api.depends('classroom_id')
    def _compute_status(self):
        for student in self:
            if student.classroom_id:
                student.status = 'active'
            elif student.status not in ['graduated', 'dropout']:
                student.status = 'draft'

    # === Override Create Method ===
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('id_student') or vals.get('id_student') == _('New'):
                vals['id_student'] = self.env['ir.sequence'].next_by_code('education.student') or _('New')
        return super().create(vals_list)

    # === Actions ===
    def action_set_to_dropout(self):
        invalid_students = self.filtered(lambda s: s.status != 'active')
        if invalid_students:
            raise ValidationError(_("Only students with 'Active' status can be dropped out."))

        for student in self:
            classroom = student.classroom_id
            if classroom and student in classroom.student_ids:
                classroom.student_ids = [(3, student.id)]

            student.write({
                'classroom_id': False,
                'status': 'dropout',
            })

            student.message_post(
                body=_("Student has been dropped out and removed from class: %s.") % (classroom.name if classroom else "-")
            )

    def action_cancel_dropout(self):
        invalid_students = self.filtered(lambda s: s.status != 'dropout')
        if invalid_students:
            raise ValidationError(_("Only students with 'Dropout' status can be reinstated."))

        for student in self:
            student.write({'status': 'draft'})
            student.message_post(
                body=_("Student dropout status has been canceled. Status changed to 'Draft'.")
            )
