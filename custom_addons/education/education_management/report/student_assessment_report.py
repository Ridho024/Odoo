from odoo import api, models

class AssessmentReport(models.AbstractModel):
    _name = 'report.education_management.report_assessment_student'

    def _get_report_values(self, docids, data=None):
        report = self.env['ir.actions.report']._get_report_from_name('education_management.report_assessment_student')
        docs = self.env[report.model].browse(docids)

        # Pastikan docs tidak kosong
        if not docs:
            raise ValueError("No student records found for report generation.")

        # Ambil semua assessment dari semua student yang dicetak
        assessment_data = self.env['student.assessment.result'].search([('student_id', 'in', docids)])

        # Struktur data kosong untuk semua student (supaya tidak error meskipun data kosong)
        grouped_assessments = {student.id: {} for student in docs}

        for assessment in assessment_data:
            student_id = assessment.student_id.id
            semester = assessment.assessment_id.semester or 'Unknown'
            category = assessment.assessment_id.category or 'Unknown'
            subject = assessment.assessment_id.subject_id.name if assessment.assessment_id.subject_id else 'Unknown'

            grouped_assessments.setdefault(student_id, {})
            grouped_assessments[student_id].setdefault(semester, {})
            grouped_assessments[student_id][semester].setdefault(category, {})
            grouped_assessments[student_id][semester][category].setdefault(subject, {'scores': [], 'average': 0.0})

            grouped_assessments[student_id][semester][category][subject]['scores'].append(assessment.score)

        # Hitung rata-rata
        for student_id, student_data in grouped_assessments.items():
            for semester, categories in student_data.items():
                for category, subjects in categories.items():
                    for subject, data in subjects.items():
                        if data['scores']:
                            data['average'] = sum(data['scores']) / len(data['scores'])

        return {
            'docs': docs,
            'assessment_data': grouped_assessments,
        }
