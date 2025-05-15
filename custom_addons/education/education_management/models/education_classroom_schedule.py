from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EducationClassroomSchedule(models.Model):
    _name = 'education.classroom.schedule'
    _description = 'Classrom Schedule'
    _rec_name = "classroom_id"

    day_of_week = fields.Selection([
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ], string='Day of Week', required=True)
    
    classroom_id = fields.Many2one(
        'education.classroom', string='Classroom', readonly=True
    )
    
    grade = fields.Selection([
        ('1', 'X'),
        ('2', 'XI'),
        ('3', 'XII'),
        ('4', 'XIII')
    ], string='Grade', readonly=True, related='classroom_id.grade', store=True)
    
    subject_id = fields.Many2one(
        'education.subject', string='Subject Name', required=True
    )
    
    teacher_id = fields.Many2one(
        'res.partner', string='Main Teacher', required=True,
        domain="[('is_teacher', '=', True)]"
    )

    start_time = fields.Float(
        string='From', required=True,
        help='Start time in 24-hour format (e.g., 9.00 for 9:00 AM)'
    )
    
    end_time = fields.Float(
        string='To', required=True,
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
