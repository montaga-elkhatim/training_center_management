from odoo import models ,fields

class Presenter(models.Model):
    _name = "presenter" 
    _description = "presenter" 
    name = fields.Char(string="Name",required=True, )
    image=fields.Binary(string="image")
    biography = fields.Text(string="Biography")
    phone = fields.Char(string="Phone",required=True)
    course_ids = fields.One2many("course","presenter_id")
    email = fields.Char(string="Email")  