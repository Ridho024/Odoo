from odoo import models, fields, api
from datetime import date, timedelta

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
    total_absent = fields.Integer(string='Total Absent', help='Total absent for month')
    total_present = fields.Integer(string='Total Present', help='Total present for month')
    total_absent_alpha = fields.Integer(string='Total Alpha', help='Total alpha for month')
    total_absent_sick = fields.Integer(string='Total Sick', help='Total sick for month')
    total_absent_permit = fields.Integer(string='Total Permit', help='Total permit for month')
    
    # Administration
    nip = fields.Char(string='NIP')
    attendance_ids = fields.One2many('attendance.record', 'teacher_id', string='Attendances Records')
    
    def compute_monthly_attendance(self):
        """ Compute total attendance for teachers at the end of the month. """
        today = date.today()
        first_day = today.replace(day=1)
        last_day = first_day - timedelta(days=1)
        first_day_of_last_month = last_day.replace(day=1)
        
        teachers = self.search([('is_teacher', '=', True)])
        for teacher in teachers:
            attendance_records = self.env['attendance.record'].search([
                ('teacher_id', '=', teacher.id),
                ('date', '>=', first_day_of_last_month),
                ('date', '<=', last_day)
            ])
            
            total_present = sum(attendance_records.mapped('present'))
            total_absent = sum(attendance_records.mapped('absent'))
            total_absent_alpha = sum(attendance_records.mapped('absent_alpha'))
            total_absent_sick = sum(attendance_records.mapped('absent_sick'))
            total_absent_permit = sum(attendance_records.mapped('absent_permit'))
            
            teacher.write({
                'total_present': total_present,
                'total_absent': total_absent,
                'total_absent_alpha': total_absent_alpha,
                'total_absent_sick': total_absent_sick,
                'total_absent_permit': total_absent_permit
            })
    
class AttendanceRecord(models.Model):
    _name = 'attendance.record'
    _description = 'Attendance Record'
    
    teacher_id = fields.Many2one('res.partner', string='Teacher', readonly=True)
    date = fields.Date(string='Date', default=fields.Date.today)
    classroom_id = fields.Many2one('education.classroom', string='Classroom')
    subject_id = fields.Many2one('education.subject', string='Subject')
    
    absent = fields.Integer(string='Absent')
    present = fields.Integer(string='Present')
    
    absent_alpha = fields.Integer(string='Alpha')
    absent_sick = fields.Integer(string='Sick')
    absent_permit = fields.Integer(string='Permit')

    # @api.depends('classroom_id', 'subject_id', 'date')
    # def _compute_monthly_totals(self):
    #     """Menghitung total present dan absent untuk satu bulan"""
    #     Attendance = self.env['education.teacher.attendance']
    #     for record in self:
    #         month_start = record.date.replace(day=1)
    #         month_end = (month_start + fields.Date().from_string('30')).replace(day=1) - fields.Date().from_string('1')

    #         attendances = Attendance.search([
    #             ('classroom_id', '=', record.classroom_id.id),
    #             ('subject_id', '=', record.subject_id.id),
    #             ('date', '>=', month_start),
    #             ('date', '<=', month_end)
    #         ])
    #         record.total_present = len(attendances.filtered(lambda a: a.attendance_status == 'present'))
    #         record.total_absent = len(attendances.filtered(lambda a: a.attendance_status == 'absent'))

    # @api.depends('classroom_id', 'subject_id', 'date')
    # def _compute_monthly_absent_reasons(self):
    #     """Menghitung total absent alpha, sick, dan permit untuk satu bulan"""
    #     Attendance = self.env['education.teacher.attendance']
    #     for record in self:
    #         month_start = record.date.replace(day=1)
    #         month_end = (month_start + fields.Date().from_string('30')).replace(day=1) - fields.Date().from_string('1')

    #         attendances = Attendance.search([
    #             ('classroom_id', '=', record.classroom_id.id),
    #             ('subject_id', '=', record.subject_id.id),
    #             ('date', '>=', month_start),
    #             ('date', '<=', month_end),
    #             ('attendance_status', '=', 'absent')
    #         ])
    #         record.total_absent_alpha = len(attendances.filtered(lambda a: a.absent_reason == 'alpha'))
    #         record.total_absent_sick = len(attendances.filtered(lambda a: a.absent_reason == 'sick'))
    #         record.total_absent_permit = len(attendances.filtered(lambda a: a.absent_reason == 'permit'))