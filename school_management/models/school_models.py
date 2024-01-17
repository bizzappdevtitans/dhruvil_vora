from odoo import fields, models


class SchoolTeacher(models.Model):
    _name = "school.teacher"
    _description = "Details of student"
    teacher_name = fields.Char(string="Name")
    teacher_age = fields.Integer(string="Age")
    teacher_email = fields.Char(string="Email")
    experience = fields.Integer(string="Teaching Experience")
    teacher_address = fields.Text(string="Address")
    is_married = fields.Boolean(string="Is Married?")
    gender = fields.Selection(
        [
            ("male", "Male"),
            ("female", "FeMale"),
            ("other", "Other"),
        ],
        string="Gender",
        default="male",
    )
    teacher_subject = fields.Selection(
        [
            ("english", "English"),
            ("gujrati", "Gujarati"),
            ("hindi", "Hindi"),
            # ("science", "Science"),
            # ("maths", "Maths"),
            # ("social_studies", "Social_studies"),
            # ("computer", "Computer"),
            # ("p.t", "P.t"),
        ],
        string="Subject",
        default="english",
    )

    def demo_button(self):
        print("nothing")

    def smart_button(self):
        return {
            "name": "Appointment",
            "res_model": "school.student",
            "view_id": False,
            "view_mode": "tree,form",
            "type": "ir.actions.act_window",
        }


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


class Teacher_detail(models.Model):
    _name = "teacher.detail"
    _description = "Details on desktop"
