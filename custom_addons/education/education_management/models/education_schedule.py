from odoo import models, fields, api

class EducationSchedule(models.Model):
    _name = 'education.schedule'
    _description = 'Class Schedule'
    _rec_name = "course_id"     
    
    course_id = fields.Many2one('education.course', string='Course', required=True)
    classroom_id = fields.Many2one('education.classroom', string='Classroom', required=True)
    teacher_id = fields.Many2one('education.teacher', string='Teacher', required=True)
    day_of_week = fields.Selection([
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ], string='Day of Week', required=True)
    start_time = fields.Float(string='Start Time', required=True, help='Start time in 24-hour format (e.g., 9.00 for 9:00 AM)')
    end_time = fields.Float(string='End Time', required=True, help='End time in 24-hour format (e.g., 11.00 for 11:00 AM)')
    duration = fields.Float(string='Duration (hours)', compute='_compute_duration', store=True)
    notes = fields.Text(string='Notes')
    
    @api.depends('start_time', 'end_time')
    def _compute_duration(self):
        for rec in self:
            if rec.start_time and rec.end_time:
                rec.duration = rec.end_time - rec.start_time
            else:
                rec.duration = 0.0