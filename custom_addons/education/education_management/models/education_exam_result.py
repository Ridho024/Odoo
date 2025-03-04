from odoo import models, fields, api

class EducationExamResult(models.Model):
    _name = "education.exam.result"
    _description = "Exam Result"

    student_id = fields.Many2one("education.student", string="Student", required=True)
    exam_id = fields.Many2one("education.exam", string="Exam", required=True)
    course_id = fields.Many2one("education.course", string="Course", related="exam_id.course_id", store=True)
    marks_obtained = fields.Float(string="Marks Obtained", required=True)
    total_marks = fields.Float(string="Total Marks", required=True)
    percentage = fields.Float(string="Percentage", compute="_compute_percentage", store=True)
    grade = fields.Selection(
        [
            ("A", "A"),
            ("B", "B"),
            ("C", "C"),
            ("D", "D"),
            ("E", "E"),
            ("F", "F"),
        ],
        string="Grade",
        compute="_compute_grade",
        store=True
    )
    status = fields.Selection(
        [("pass", "Pass"), ("fail", "Fail")],
        string="Status",
        compute="_compute_status",
        store=True
    )
    remark = fields.Text(string="Remarks")

    @api.depends("marks_obtained", "total_marks")
    def _compute_percentage(self):
        for record in self:
            if record.total_marks:
                record.percentage = (record.marks_obtained / record.total_marks) * 100
            else:
                record.percentage = 0.0

    @api.depends("percentage")
    def _compute_grade(self):
        for record in self:
            if record.percentage >= 90:
                record.grade = "A"
            elif record.percentage >= 80:
                record.grade = "B"
            elif record.percentage >= 70:
                record.grade = "C"
            elif record.percentage >= 60:
                record.grade = "D"
            elif record.percentage >= 50:
                record.grade = "E"
            else:
                record.grade = "F"

    @api.depends("grade")
    def _compute_status(self):
        for record in self:
            record.status = "pass" if record.grade in ["A", "B", "C", "D", "E"] else "fail"
