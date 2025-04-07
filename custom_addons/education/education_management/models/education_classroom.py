from odoo import models, fields, api, _

class EducationClassroom(models.Model):
    _name = 'education.classroom'
    _description = 'Classroom Information'
    _sql_constraints = [
        ('name', 'unique(name)', 'Classroom with this name is already exist!'),
    ]
    
    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True, copy=False, readonly=True, index=True, default='New')
    grade = fields.Selection([('1', 'X'), ('2', 'XI'), ('3', 'XII'), ('4', 'XIII')], string='Grade', required=True)
    capacity = fields.Integer(string='Capacity', required=True, help='Maximum number of students allowed in the class')
    teacher_id = fields.Many2one('res.partner', string='Teacher', help='Main teacher responsible for class', domain="[('is_teacher', '=', True)]")
    student_ids = fields.Many2many('education.student', string='Enrolled Student', domain="[('classroom_id', '=', False)]")
    major_id = fields.Many2one('education.major', string='Class Major')
    schedule_ids = fields.One2many('education.schedule', 'classroom_id', string='Class Schedule')
    active = fields.Boolean(string='Active', default=True)
    color = fields.Integer(string='Color')
    
    @api.model
    def create(self, vals):
        # Set code jika belum ada
        if vals.get('code', _('New')) == _('New'):
            vals['code'] = self.env['ir.sequence'].next_by_code('education.classroom') or _('New')

        # Ambil dan proses student_ids sebelum create
        student_operations = vals.get('student_ids', [])

        # Buat record classroom
        classroom = super().create(vals)

        if student_operations:
            student_env = self.env['education.student']
            linked_student_ids = []

            for op in student_operations:
                if op[0] == 6:
                    linked_student_ids.extend(op[2])
                elif op[0] == 4:
                    linked_student_ids.append(op[1])

            if linked_student_ids:
                students = student_env.browse(linked_student_ids)
                students.write({'classroom_id': classroom.id})

        return classroom

    
    def write(self, vals):
        """Pastikan classroom_id pada siswa diperbarui jika student_ids berubah."""
        for classroom in self:
            old_students = classroom.student_ids

            res = super().write(vals)

            if 'student_ids' in vals:
                student_ops = vals['student_ids']
                student_env = self.env['education.student']
                new_student_ids = set()
                removed_student_ids = set()

                for op in student_ops:
                    if op[0] == 6:  # Replace all
                        new_ids = set(op[2])
                        new_student_ids |= new_ids
                        removed_student_ids |= set(old_students.ids) - new_ids
                    elif op[0] == 4:  # Add
                        new_student_ids.add(op[1])
                    elif op[0] == 3:  # Remove
                        removed_student_ids.add(op[1])
                    elif op[0] == 5:  # Unlink all
                        removed_student_ids |= set(old_students.ids)

                if new_student_ids:
                    student_env.browse(list(new_student_ids)).write({'classroom_id': classroom.id})
                if removed_student_ids:
                    student_env.browse(list(removed_student_ids)).write({'classroom_id': False})

        return res

