from odoo import fields, models, api
from odoo.exceptions import ValidationError


# course class
class SchoolCourse(models.Model):
    _name = "school.course"
    _description = "Details of Course"
    _rec_name = "course_name"
    teacher_id = fields.Many2one("school.teacher", string="Teacher")
    course_name = fields.Char(string="Course Name", required=True)
    course_upload_date = fields.Datetime(
        string="Upload Date", default=fields.Datetime.now
    )
    description = fields.Html(string="Description")
    teacher_count = fields.Integer(
        string="Teacher Count",
    )
