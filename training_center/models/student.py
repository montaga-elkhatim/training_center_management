from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Student(models.Model):
    _name = 'student'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "student"
    name = fields.Char(string="student Name", traking=True)  
    gender = fields.Selection([
        ('male','Male'),
        ('female','Female')
    ],string="Gender",required=True)
    phone = fields.Char(string="Phone",required=True,digits='14')
    age = fields.Integer(string="Age")
    course_ids= fields.Many2many("course",string="courses")  
    email = fields.Char(string="Email")   
    
    @api.model_create_multi
    def create(self,vals): 
        res = super(Student,self).create(vals) 
        for records in res.course_ids:
            if records.reserved_seats < records.num_seats:
                records.reserved_seats = records.reserved_seats+1
            elif records.reserved_seats == records.num_seats: 
                res.course_ids.reg_state ="closed"
            else:
                raise ValidationError(("'%s' Course Is Closed" % records.name))
        return res
    @api.model
    def write(self,vals):
        course_pre = self.course_ids
        print(course_pre)
        res = super(Student,self).write(vals)
        for records in self.course_ids:
            if records in course_pre:
                pass
            else:
                if records.reserved_seats < records.num_seats:
                    records.reserved_seats = records.reserved_seats+1
                elif records.reserved_seats == records.num_seats:
                    records.reserved_seats = records.reserved_seats+1
                    self.course_ids.reg_state ="closed"
                else:
                    raise ValidationError(("'%s' Course Is Closed" % records.name))
        
        print(self.course_ids)
        return res