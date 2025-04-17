from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EducationSchedule(models.Model):
    _name = 'education.schedule'
    _description = 'Class Schedule'
    _rec_name = "subject_id"

    subject_id = fields.Many2one(
        'education.subject', string='Subject Name', required=True
    )
    classroom_id = fields.Many2one(
        'education.classroom', string='Classroom', readonly=True
    )
    teacher_id = fields.Many2one(
        'res.partner', string='Teacher', required=True,
        domain="[('is_teacher', '=', True)]"
    )
    day_of_week = fields.Selection([
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ], string='Day of Week', required=True)

    start_time = fields.Float(
        string='Start Time', required=True,
        help='Start time in 24-hour format (e.g., 9.00 for 9:00 AM)'
    )
    end_time = fields.Float(
        string='End Time', required=True,
        help='End time in 24-hour format (e.g., 11.00 for 11:00 AM)'
    )
    duration = fields.Float(
        string='Duration (hours)', compute='_compute_duration', store=True
    )
    notes = fields.Text(string='Notes')

    @api.depends('start_time', 'end_time')
    def _compute_duration(self):
        for rec in self:
            if rec.start_time is not None and rec.end_time is not None:
                rec.duration = max(0.0, rec.end_time - rec.start_time)
            else:
                rec.duration = 0.0

    @api.constrains('start_time', 'end_time')
    def _check_time_validity(self):
        for rec in self:
            if rec.start_time >= rec.end_time:
                raise ValidationError("In classroom, end time must be greater than start time.")
