from odoo import models, fields

class Room(models.Model):
    _name = "room" 
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Room" 

    name = fields.Char(string="Name") 
    setting_number = fields.Integer(string= "Setting Number")  
    sessions_ids = fields.Many2many("session", string="session")  