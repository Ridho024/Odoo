from odoo import api, models

class AssessmentReport(models.AbstractModel):
    _name = 'report.education_management.report_assessment_student'
    
    def _get_report_values(self, docids, data=None):
        report = self.env['ir.actions.report']._get_report_from_name('education_management.report_assessment_student')
        
        docs = self.env[report.model].browse(docids)
        
        assessment_data = self.env['assessment.result'].search([('student_id', '=', docids)])
        
        # Struktur data untuk menyimpan hasil
        grouped_assessments = {}

        # Mengelompokkan berdasarkan semester, kategori, dan subject
        for assessment in assessment_data:
            semester = assessment.semester or 'Unknown'
            category = assessment.category or 'Unknown'
            subject = assessment.subject_id.name if assessment.subject_id else 'Unknown'

            # Membuat struktur dictionary bertingkat
            if semester not in grouped_assessments:
                grouped_assessments[semester] = {}

            if category not in grouped_assessments[semester]:
                grouped_assessments[semester][category] = {}

            if subject not in grouped_assessments[semester][category]:
                grouped_assessments[semester][category][subject] = {'scores': [], 'average': 0.0}

            # Menambahkan nilai ke daftar skor
            grouped_assessments[semester][category][subject]['scores'].append(assessment.score)

        # Hitung rata-rata untuk setiap grup
        for semester, categories in grouped_assessments.items():
            for category, subjects in categories.items():
                for subject, data in subjects.items():
                    if data['scores']:
                        data['average'] = sum(data['scores']) / len(data['scores'])
        
        return {
            'docs': docs,
            'assessment_data': grouped_assessments,
        }