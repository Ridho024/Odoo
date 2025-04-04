from odoo import models

class StudentAttendanceReport(models.AbstractModel):
    _name = 'report.education_management.report_student_attendance'

    def _get_report_values(self, docids, data=None):
        report = self.env['ir.actions.report']._get_report_from_name('education_management.report_student_attendance')

        docs = self.env[report.model].browse(docids)
        
        attendance_data = self.env['education.student.attendance'].search([('student_id', '=', docids)])
        grouped_attendance = {}
        
        for attendance in attendance_data:
            year = attendance.date.strftime('%Y')  # Tahun (contoh: 2025)
            month = attendance.date.strftime('%B')  # Nama bulan (contoh: Januari)
            subject = attendance.subject_id.name if attendance.subject_id else 'Unknown'  # Nama mata pelajaran
            status = attendance.status or 'Unknown'  # Status (Present/Absent)
            reason = attendance.absent_reason or 'Unknown'  # Alasan absen (Permit/Sick/Alpha)

            # Inisialisasi jika tahun belum ada
            if year not in grouped_attendance:
                grouped_attendance[year] = {}

            # Inisialisasi jika bulan belum ada dalam tahun tertentu
            if month not in grouped_attendance[year]:
                grouped_attendance[year][month] = {}

            # Inisialisasi jika mata pelajaran belum ada dalam bulan tertentu
            if subject not in grouped_attendance[year][month]:
                grouped_attendance[year][month][subject] = {
                    'present': 0,
                    'absent': 0,
                    'reasons': {
                        'permit': 0,
                        'sick': 0,
                        'alpha': 0
                    }
                }

            # Hitung jumlah hadir dan absen
            if status == 'present':
                grouped_attendance[year][month][subject]['present'] += 1
            elif status == 'absent':
                grouped_attendance[year][month][subject]['absent'] += 1
                if reason in grouped_attendance[year][month][subject]['reasons']:
                    grouped_attendance[year][month][subject]['reasons'][reason] += 1

        return {
            'docs': docs,
            'attendance_data': grouped_attendance,
        }