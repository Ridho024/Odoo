from odoo import models
from collections import defaultdict

class EvaluationReport(models.AbstractModel):
    _name = 'report.education_management.report_evaluation_teacher'
    
    def _get_report_values(self, docids, data=None):
        report = self.env['ir.actions.report']._get_report_from_name('education_management.report_evaluation_teacher')
        docs = self.env[report.model].browse(docids)
        
        evaluation_data = self.env['teacher.evaluation'].search([('teacher_id', '=', docids)])
        grouped_evaluations = defaultdict(lambda: defaultdict(lambda: {'results': [], 'feedback': []}))
        
        for evaluation in evaluation_data:
            month = evaluation.date.strftime('%B %Y')
            name = evaluation.name
            
            # Simpan hasil evaluasi dan feedback
            grouped_evaluations[month][name]['results'] = evaluation.evaluation_result_ids
            grouped_evaluations[month][name]['feedback'] = evaluation.feedback_ids
        
        return {
            'docs': docs,
            'evaluation_data': dict(grouped_evaluations), # Konversi defaultdict ke dict
        }