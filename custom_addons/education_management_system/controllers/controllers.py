# -*- coding: utf-8 -*-
# from odoo import http


# class EducationManagementSystem(http.Controller):
#     @http.route('/education_management_system/education_management_system', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/education_management_system/education_management_system/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('education_management_system.listing', {
#             'root': '/education_management_system/education_management_system',
#             'objects': http.request.env['education_management_system.education_management_system'].search([]),
#         })

#     @http.route('/education_management_system/education_management_system/objects/<model("education_management_system.education_management_system"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('education_management_system.object', {
#             'object': obj
#         })

