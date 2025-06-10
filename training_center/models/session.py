from odoo import models, fields

class Session(models.Model):
    _name = 'session' 
    _description = "session"
    session_name = fields.Char(string="Session Name")  
    session_course = fields.Many2one("course", string="Course Name")  
    session_presenter = fields.Many2one("presenter", string="Presenter Name")  
    session_room = fields.Many2one("room", string="Session Room")  
    session_date = fields.Char(string="Session Date")  
     