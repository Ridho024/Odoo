from odoo import models, fields

class Classroom(models.Model):
    _name = 'classroom.classroom'
    _description = 'Classroom'
    
    name = fields.Char(string='Kode Ruangan', required=True, help='Nama ruangan.')
    floor = fields.Integer(string='Lantai', required=True, help='Lantai ruangan.')
    room_number = fields.Integer(string='Nomor Ruangan', required=True, help='Nomor ruangan.')
    capacity = fields.Integer(string='Kapasitas', required=True, help='Kapasitas ruangan.')