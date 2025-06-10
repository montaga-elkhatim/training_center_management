from odoo import models, fields, api
from datetime import  timedelta, time, datetime
from odoo.exceptions import ValidationError 

class Course(models.Model):
    _name = "course"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "course"
    name = fields.Char(string="Name", required=True, default="New Course", copy=False, tracking=True) 
    state = fields.Selection([
        ('registration','Registration'),
        ('registration_closed','Registration Closed'),
        ('in_progress','In Progress'),
        ('finished','Finished')
    ],string= "State", default= "registration" )
    reg_state = fields.Selection([
        ('open','Open'),
        ('closed','Closed'), 
    ],string="Registration State",default= "open" )
    description = fields.Text(string="Description")
    presenter_id = fields.Many2one("presenter", required=True)
    department_type = fields.Selection([
        ('technical' , 'Technical'),
        ('healthy' , 'Healthy'),
        ('humanskill' , 'Human Skill'),
        ('languages' , 'Languages'),
        ],string ="Department",required =True,default="technical")
    image = fields.Binary(string="Image")
    postcode = fields.Integer(string="Postcode")
    price = fields.Integer(string="Price")  
    sessions = fields.Integer(compute="_compute_sessions", string="Sessions", default="10")  
    need = fields.Char(string="Need")
    registration_deadline = fields.Date(string="Registration Deadline")
    start_date = fields.Date(string="Start of study")
    end_date = fields.Date(string="End of study" ) 
    duration_study = fields.Integer(string="Study hours" ,default="20" )
    duration_study_by_week = fields.Integer(string="Study hours per day",default="2")
    num_seats = fields.Integer(string="Number of Seats" , default="10" )
    reserved_seats = fields.Integer(string="Reserved Seats", default="0") 
    study_type = fields.Selection([
        ('offline','Offline'),
        ('online','Online'),
        ('combined','Combined')
        ],string = "Study Type",default = "offline")
    certificate = fields.Char(string="Certificate")
    batch = fields.Integer(string="Batch Number" ) 
    student_ids = fields.Many2many("student" ,string= "Students")
    session_time = fields.Date(strsing="Session Time") 
    room_id = fields.Many2one("room", string="Room", required=True)
    _sql_constraints = [
        ("name_uniq", "unique(name)", "The name of course must be unique!"),
        ]
    
    @api.onchange("duration_study","duration_study_by_week")
    def _compute_sessions(self): 
        for rec in self:
            if rec.duration_study and rec.duration_study_by_week:
                rec.sessions = rec.duration_study // rec.duration_study_by_week

   

    @api.onchange("sessions","start_date","registration_deadline")
    def _compute_end_date(self):
        for rec in self: 
                if rec.start_date:
                    rec.end_date = rec.start_date + timedelta(days=rec.sessions-1)
        print("inside check_state")
        for record in self:
            if record.registration_deadline and record.start_date and record.end_date :
                if fields.Date.today() <= record.registration_deadline :
                    record.state = "registration"  
                    record.reg_state = "open"  
                elif fields.Date.today() > record.registration_deadline and fields.Date.today()< record.start_date :
                    record.reg_state = "closed"
                    record.state = "registration_closed"  
                elif fields.Date.today() >= record.start_date :
                    record.state = "in_progress"
                if fields.Date.today() > record.end_date:
                    record.state = "finished" 
    @api.model_create_multi
    def create(self, vals): 
        course = super(Course, self).create(vals)  
        print("inside create_session")
        # course_room = course.env["room"].search([('id','=',course.room_id.id)])
        for i in range(course.sessions):
            new_session = course.env['session'].create([{
                    'session_name' : f'session {i+1}', 
                    'session_course' : course.id, 
                    'session_presenter' : course.presenter_id.id, 
                    'session_room' : course.room_id.id , 
                    'session_date' : course.start_date , 
                        
            }])
            # print(course_room)
            # course_room.sessions_ids ={"sessions_ids" : new_session.id}         
            course.start_date = course.start_date + timedelta(days=1)
        
        return course 
    
    def unlink(self):
        for rec in self:
            delete_rec = rec.env['session'].search([('session_course.name','=',rec.name)])
            if delete_rec:
                print("exist record")
                delete_rec.unlink()
        res = super(Course,self).unlink()
        return res 
 
    

      
    @api.constrains("registration_deadline","start_date","end_date")
    def _check_date(self):
        for record in self:
            if not( record.registration_deadline < record.start_date ):
                raise ValidationError("study Date and Start of study Date must be after Registration Deadline Date")
   
    @api.depends("student_ids")
    def compute_reserved_seats(self):
        for rec in self:
            rec.reserved_seats=len(rec.student_ids)
    @api.model
    def check_state(self): 
        records = self.env['course'].search([])
        print("inside check_state")
        for record in records:
            if fields.Date.today() <= record.registration_deadline :
                record.state = "registration"  
            elif fields.Date.today() > record.registration_deadline and fields.Date.today()< record.start_date :
                record.reg_state = "closed"
                record.state = "registration_closed"  
            elif fields.Date.today() >= record.start_date :
                record.state = "in_progress"
            if fields.Date.today() > record.end_date:
                record.state = "finished"  