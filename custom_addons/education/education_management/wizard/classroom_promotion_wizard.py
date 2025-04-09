from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ClassroomPromotionWizard(models.TransientModel):
    _name = 'classroom.promotion.wizard'
    _description = 'Classroom Promotion Wizard'
    
    current_classroom_id = fields.Many2one('education.classroom', string='Classroom', required=True)
    new_classroom_id = fields.Many2one('education.classroom', string='New Classroom', domain="[('id', '!=', current_classroom_id)]")
    student_ids = fields.Many2many('education.student', string='Students to Promote', required=True, related='current_classroom_id.student_ids')
    show_graduate_button = fields.Boolean(string='Show Graduate Button', compute='_compute_show_graduate_button')
    
    @api.depends('current_classroom_id.grade')
    def _compute_show_graduate_button(self):
        for wizard in self:
            wizard.show_graduate_button = wizard.current_classroom_id.grade in ('3', '4')
            
    def action_graduate_students(self):
        self.ensure_one()
        
        if not self.student_ids:
            raise UserError(_("No students to graduate."))
        
        self.current_classroom_id.student_ids = [(3, student.id) for student in self.student_ids]
        self.student_ids.write({'status': 'graduated'})
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Graduation Complete 🎓'),
                'message': _('%s students have graduated.') % len(self.student_ids),
                'sticky': False,
                'type': 'success',
            },
            'rainbowman': 'graduation',
        }
    
    def action_promote_students(self):
        self.ensure_one()
        
        if self.new_classroom_id.student_ids:
            raise UserError(_(
                "The selected classroom already has students. Please choose another classroom."
                "Please move or clear them before promoting new students."
                ) % self.new_classroom_id.name)
        
        if not self.student_ids:
            raise UserError(_("Please select at least one student to promote."))
        
        if not self.new_classroom_id:
            raise UserError(_("Please select a new classroom for the promotion."))
        
        # Hapus siswa dari kelas saat ini
        self.current_classroom_id.student_ids = [(3, student.id) for student in self.student_ids]
        self.new_classroom_id.student_ids = [(4, student.id) for student in self.student_ids]
         
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Promotion Successful'),
                'message': _('%s students were promoted to %s.') % (
                    len(self.student_ids),
                    self.new_classroom_id.name,
                ),
                'sticky': False,
                'type': 'success',
            },
        } 