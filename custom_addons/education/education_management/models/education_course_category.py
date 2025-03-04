from odoo import models, fields

class EducationCourseCategory(models.Model):
    _name = 'education.course.category'
    _description = 'Course Category'
    
    name = fields.Char(string="Category Name", required=True)
    code = fields.Char(string="Category Code")
    description = fields.Text(string="Description")
    parent_id = fields.Many2one("education.course.category", string="Parent Category")
    child_ids = fields.One2many("education.course.category", "parent_id", string="Subcategories")
    course_ids = fields.One2many("education.course", "category_id", string="Courses")
    active = fields.Boolean(string="Active", default=True)
