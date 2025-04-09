from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class EducationStudent(models.Model):
    _name = 'education.student'
    _description = 'Education Student'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence'
    
    # === Basic Information ===
    sequence = fields.Integer(string='Sequence')
    name = fields.Char(string='Student Name', required=True, tracking=True, default="John Doe")
    nisn = fields.Char(string='NISN', required=True, tracking=True)
    id_student = fields.Char(string='Student ID', required=True, copy=False, readonly=True, index=True, default='New', tracking=True)
    date_of_birth = fields.Date(string='Date of Birth', tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string='Gender', tracking=True)
    email = fields.Char(string='Student Email', tracking=True)
    phone = fields.Char(string='Student Phone', tracking=True)
    photo = fields.Image(string='Photo')
    
    # === Parent Info ===
    father_name = fields.Char(string='Father Name', tracking=True)
    father_contact = fields.Char(string='Father Contact', tracking=True)
    father_email = fields.Char(string='Father Email', tracking=True)
    mother_name = fields.Char(string='Mother Name', tracking=True)
    mother_contact = fields.Char(string='Mother Contact', tracking=True)
    mother_email = fields.Char(string='Mother Email', tracking=True)
    
    # === Academic Info ===
    classroom_id = fields.Many2one('education.classroom', string='Class', tracking=True, readonly=True)
    
    # === Status ===
    status = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('graduated', 'Graduated'),
        ('dropout', 'Dropout'),
    ], string='Status', tracking=True, compute='_compute_status', store=True)
    
    # === Achievement ===
    achievement_ids = fields.One2many('education.student.achievement', 'student_id', string='Academic Achievement', tracking=True)
    
    # === Computed Fields ===
    @api.depends('classroom_id')
    def _compute_status(self):
        for student in self:
            if student.classroom_id:
                student.status = 'active'
        
    @api.model_create_multi
    def create(self,vals_list):
        """Generate unique Student ID"""
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

            # Hapus dari Many2many classroom.student_ids jika ada
            if classroom and student in classroom.student_ids:
                classroom.student_ids = [(3, student.id)]

            # Reset classroom dan ubah status
            student.write({
                'classroom_id': False,
                'status': 'dropout',
            })

            # Optional logging
            student.message_post(
                body=_("Student has been dropped out and removed from class: %s.") % (classroom.name if classroom else "-")
            )

    def action_cancel_dropout(self):
        invalid_students = self.filtered(lambda s: s.status != 'dropout')
        if invalid_students:
            raise ValidationError(_("Only students with 'Dropout' status can be reinstated."))

        for student in self:
            student.write({
                'status': 'draft',
            })

            # Opsional: kirim pesan ke chatter
            student.message_post(
                body=_("Student dropout status has been canceled. Status changed to 'Draft'.")
            )