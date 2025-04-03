# -*- coding: utf-8 -*-
# from odoo import http


# class EducationManagement(http.Controller):
#     @http.route('/education_management/education_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/education_management/education_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('education_management.listing', {
#             'root': '/education_management/education_management',
#             'objects': http.request.env['education_management.education_management'].search([]),
#         })

#     @http.route('/education_management/education_management/objects/<model("education_management.education_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('education_management.object', {
#             'object': obj
#         })

