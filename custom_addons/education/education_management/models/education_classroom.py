from odoo import models, fields, api

class EducationClassroom(models.Model):
    _name = 'education.classroom'
    _description = 'Classroom Information'
    
    name = fields.Char(string='Classroom Name', required=True)
    code = fields.Char(string='Class Code', required=True, copy=False, readonly=True, default=lambda self: self.env['ir.sequence'].next_by_code('education.classroom') or 'New')
    capacity = fields.Integer(string='Capacity', required=True, help='Maximum number of students allowed in the class')
    teacher_id = fields.Many2one('education.teacher', string='Homeroom Teacher', help='Main teacher responsible for class')
    student_ids = fields.Many2many('education.student', string='Enrolled Student', domain="[('classroom_id', '=', False)]")
    subject_ids = fields.Many2many('education.course', string='Subjects Taught')
    schedule_ids = fields.One2many('education.schedule', 'classroom_id', string='Class Schedule')
    location = fields.Char(string='Location', help='Classroom location in the school building')
    active = fields.Boolean(string='Active', default=True)
    academic_year = fields.Char(string='Academic Year')
    color = fields.Integer(string='Color')
    
    def write(self, vals):
        """Memastikan classroom_id diperbarui saat student_ids berubah"""
        for classroom in self:
            old_students = classroom.student_ids  # Simpan daftar siswa sebelum perubahan
            
            res = super(EducationClassroom, classroom).write(vals)
    
            if 'student_ids' in vals:
                student_operations = vals['student_ids']
                student_env = self.env['education.student']
                
                added_students = student_env.browse([op[1] for op in student_operations if op[0] == 4])
                removed_students = student_env.browse([op[1] for op in student_operations if op[0] == 3])
                
                if added_students:
                    added_students.write({'classroom_id': classroom.id})
                
                if removed_students:
                    removed_students.write({'classroom_id': False})
                
                if any(op[0] == 6 for op in student_operations):
                    new_students = student_env.browse(student_operations[0][2])
                    new_students.write({'classroom_id': classroom.id})
                    (old_students - new_students).write({'classroom_id': False})
                
                if any(op[0] == 5 for op in student_operations):
                    old_students.write({'classroom_id': False})
    
        return res
