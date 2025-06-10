{
    "name" : "Faread Training Center ",
    "version" : "1.0.1",
    "author" : "montaga mohammed",
    "summary" : "this modual for training center ",
    "license" : "LGPL-3" ,
    "website" : "www.fareadcenter.com",
    "depends" : [
        "base",
        "mail"
        ],
    "data" : [
        "security/ir.model.access.csv",  

        "views/base_menu.xml",
        "views/course_view.xml",
        "views/student_view.xml",
        "views/presenter_view.xml", 
        "views/session_view.xml",  
        "views/room_view.xml",   

        "report/student_report.xml",
        "report/attendance_report.xml", 
        ],
    "assets" : {
        "web.assets_backend":[
            "training_center/static/src/css/main.css",
            "training_center/static/src/css/fonts.css",
        ]
    },
    "application" : True,

}