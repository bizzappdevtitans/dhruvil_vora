from odoo import fields, models


# teacher class
class SchoolTeacher(models.Model):
    _name = "school.teacher"
    _description = "Details of student"
    _rec_name = "teacher_name"
    teacher_name = fields.Char(string="Name")
    teacher_age = fields.Integer(string="Age")
    teacher_email = fields.Char(string="Email")
    experience = fields.Integer(string="Teaching Experience")
    # count_subject = fields.Integer(default=3)
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
    #    subjects_list = fields.Many2many(("english", "Gujarati"), string="Subjects")
    teacher_record_updated = fields.Date(
        "Last Updated", required=True, default=fields.datetime.now(), readonly=True
    )
    course_count = fields.Integer(
        string="Course Count", compute="_compute_course_count"
    )

    def _compute_course_count(self):
        for res in self:
            course_count = self.env["school.course"].search_count(
                [("teacher_id", "=", res.id)]
            )
            print("course count:=")
            print(course_count)
            print("value is here :=")
            print(res)
            res.course_count = course_count

    def demo_button(self):
        print("nothing")

    def smart_button(self):
        return {
            "name": "Teacher Course",
            "res_model": "school.course",
            "view_id": False,
            "view_mode": "tree,form",
            "domain": [("teacher_id", "=", self.id)],
            "type": "ir.actions.act_window",
        }

    def action_delete_2(self):
        # self.write({"teacher_record_updated": fields.Date.today()})
        # self.write({"teacher_address": "today"})
        super(SchoolTeacher, self).unlink()
        return {
            "name": "teacher",
            "res_model": "school.teacher",
            "view_id": False,
            "view_mode": "tree,form",
            "type": "ir.actions.act_window",
        }


# course class
class SchoolCourse(models.Model):
    _name = "school.course"
    _description = "Details of Course"

    teacher_id = fields.Many2one("school.teacher", string="Teacher")
    course_name = fields.Char(string="Course Name", required=True)
    course_upload_date = fields.Datetime(
        string="Upload Date", default=fields.Datetime.now
    )
    first_name = fields.Char(string="First Name")
    description = fields.Html(string="Description")
    teacher_count = fields.Integer(
        string="Teacher Count",
    )


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


# extra details of teacher need to work on
class Teacher_detail(models.Model):
    _name = "teacher.detail"
    _description = "Details on desktop"
