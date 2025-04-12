from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EducationSubjectDetail(models.Model):
    _name = 'education.subject.detail'
    _description = 'Subject Detail'
    _rec_name = 'studies'

    subject_id = fields.Many2one('education.subject', string='Subject', required=True, ondelete='cascade')
    curriculum_id = fields.Many2one('education.major.curriculum', string='Curriculum', required=True)
    studies = fields.Text(string='Lesson / Study Material', required=True)

    @api.constrains('curriculum_id')
    def _check_curriculum(self):
        for record in self:
            if record.curriculum_id and not isinstance(record.curriculum_id.id, int):
                raise ValidationError("Please select a valid curriculum from the list. Manual input is not allowed.")