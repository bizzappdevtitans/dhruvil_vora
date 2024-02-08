from odoo import fields, models, api
from odoo.exceptions import ValidationError


# student class
class SchoolStudent(models.Model):
    _name = "school.student"
    _description = "Details of student"
    student_name = fields.Char(string="Name")
    student_age = fields.Integer(string="Age")
    student_email = fields.Char(string="Email")
    student_address = fields.Text(string="Address")
    gender = fields.Selection(
        [
            ("male", "Male"),
            ("female", "FeMale"),
            ("other", "Other"),
        ],
        string="Gender",
        default="male",
    )
