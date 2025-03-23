# -*- coding: utf-8 -*-
# from odoo import http


# class EducationAssessment(http.Controller):
#     @http.route('/education_assessment/education_assessment', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/education_assessment/education_assessment/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('education_assessment.listing', {
#             'root': '/education_assessment/education_assessment',
#             'objects': http.request.env['education_assessment.education_assessment'].search([]),
#         })

#     @http.route('/education_assessment/education_assessment/objects/<model("education_assessment.education_assessment"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('education_assessment.object', {
#             'object': obj
#         })

