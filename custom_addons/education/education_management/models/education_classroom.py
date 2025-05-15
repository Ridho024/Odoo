from odoo import models, fields, api, _

class EducationClassroom(models.Model):
    _name = 'education.classroom'
    _description = 'Classroom Information'
    _sql_constraints = [
        ('name', 'unique(name)', 'Classroom with this name already exists!'),
    ]

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True, copy=False, readonly=True, index=True, default='New')
    grade = fields.Selection([
        ('1', 'X'),
        ('2', 'XI'),
        ('3', 'XII'),
        ('4', 'XIII')
    ], string='Grade', required=True)
    capacity = fields.Integer(string='Capacity', required=True, help='Maximum number of students allowed in the class')
    teacher_id = fields.Many2one('res.partner', string='Teacher', domain="[('is_teacher', '=', True)]", help='Main teacher responsible for the class')
    student_ids = fields.Many2many('education.student', string='Enrolled Students', domain="[('classroom_id', '=', False)]")
    major_id = fields.Many2one('education.major', string='Class Major')
    schedule_ids = fields.One2many('education.classroom.schedule', 'classroom_id', string='Class Schedule')
    active = fields.Boolean(string='Active', default=True)
    color = fields.Integer(string='Color')

    @api.model
    def create(self, vals):
        """Generate unique code and assign classroom_id to selected students."""
        if vals.get('code', _('New')) == _('New'):
            vals['code'] = self.env['ir.sequence'].next_by_code('education.classroom') or _('New')

        classroom = super().create(vals)
        self._update_students_classroom(vals.get('student_ids'), classroom.id)

        return classroom

    def write(self, vals):
        """Update classroom_id for added/removed students."""
        for classroom in self:
            old_student_ids = classroom.student_ids.ids
            res = super().write(vals)

            if 'student_ids' in vals:
                ops = vals['student_ids']
                new_ids, removed_ids = self._extract_student_changes(ops, old_student_ids)
                student_env = self.env['education.student']

                if new_ids:
                    student_env.browse(list(new_ids)).write({'classroom_id': classroom.id})
                if removed_ids:
                    student_env.browse(list(removed_ids)).write({'classroom_id': False})

        return res

    def _update_students_classroom(self, student_ops, classroom_id):
        """Assign classroom_id to students during create."""
        if not student_ops:
            return

        student_ids = []
        for op in student_ops:
            if op[0] == 6:
                student_ids = op[2]
                break  # Replace all, so skip others
            elif op[0] == 4:
                student_ids.append(op[1])

        if student_ids:
            self.env['education.student'].browse(student_ids).write({'classroom_id': classroom_id})

    def _extract_student_changes(self, ops, old_ids):
        """Return sets of new and removed student IDs based on M2M operations."""
        new_ids = set()
        removed_ids = set()

        for op in ops:
            if op[0] == 6:  # Replace all
                new_set = set(op[2])
                new_ids |= new_set
                removed_ids |= set(old_ids) - new_set
            elif op[0] == 4:  # Add
                new_ids.add(op[1])
            elif op[0] == 3:  # Remove
                removed_ids.add(op[1])
            elif op[0] == 5:  # Unlink all
                removed_ids |= set(old_ids)

        return new_ids, removed_ids
