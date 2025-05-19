from odoo import models, fields

class EducationLibrary(models.Model):
    _name = 'education.library'
    _description = 'School Library Information'
    _rec_name = "product_id"

    product_id = fields.Many2one('product.template', string='Book Name', required=True, domain="[('categ_id', '=', 'Library Books')]")
    stock_location_id = fields.Many2one('stock.location', string='Location', required=True, domain="[('storage_category_id', '=', 'Library Shelf')]")
    row = fields.Integer(string='Row Number', required=True)
    book_genre_ids = fields.Many2many('library.book.genre', string='Book Genre')
    user_id = fields.Many2one('res.users', string='Admin', required=True)
    book_borrower_ids = fields.One2many(
        'book.borrower', 'library_id', string='Book Borrower'
    )
    
class BookBorrower(models.Model):
    _name = 'book.borrower'
    _description = 'Borrower Books Information'
    _rec_name = "book_id"
     
    library_id = fields.Many2one('education.library', string='Library Name', required=True, readonly=True)
    book_id = fields.Many2one('education.library', string='Book Name', required=True)
    student_id = fields.Many2one('education.student', string='Student Name', required=True)
    date_borrowed = fields.Date(string='Date Borrowed', default=fields.Date.today())
    expected_return = fields.Date(string='Expected Return')
    is_returned = fields.Boolean(string='Is Returned', default=False)
     
class LibraryBookGenre(models.Model):
    _name = 'library.book.genre'
    _description = 'Library Book Genre'

    name = fields.Char(string='Genre Name', required=True)
    color = fields.Integer(string='Color')