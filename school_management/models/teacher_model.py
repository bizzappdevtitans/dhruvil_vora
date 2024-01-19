from odoo import fields, models, api
from odoo.exceptions import ValidationError


# teacher class
class SchoolTeacher(models.Model):
    _name = "school.teacher"
    _description = "Details of teacher"
    _rec_name = "teacher_name"
    teacher_name = fields.Char(string="Name")
    teacher_age = fields.Integer(string="Age")
    teacher_email = fields.Char(string="Email")
    experience = fields.Float(string="Teaching Experience", digits=(2, 1))
    teacher_address = fields.Text(string="Address")
    is_married = fields.Boolean(string="Is Married?")
    teacher_courses = fields.One2many(
        "school.course", inverse_name="teacher_id", string="Courses"
    )
    gender = fields.Selection(
        [
            ("male", "Male"),
            ("female", "FeMale"),
            ("other", "Other"),
        ],
        string="Gender",
        default="male",
    )
    teacher_state = fields.Selection(
        [("class", "Class"), ("work", "Work"), ("staffroom", "Staffroom")],
        string="Status",
        default="class",
    )

    teacher_record_updated = fields.Date(
        "Last Updated", required=True, default=fields.datetime.now(), readonly=True
    )
    # task_count = fields.Integer(string="Task", compute="_compute_task_count")

    course_count = fields.Integer(
        string="Course Count", compute="_compute_course_count"
    )

    @api.constrains("experience", "teacher_age")
    def check_age_and_experience(self):
        # for example the age of retirement in about 60 and the teacher
        # started teaching from 18 then also it can't be more than 42
        if self.experience > 42:
            raise ValidationError(("The entered Experience is not accepted"))
        if self.teacher_age > 60 or self.teacher_age < 18:
            raise ValidationError(("The entered age is not suitable for teaching"))

    def _compute_course_count(self):
        for res in self:
            course_count = self.env["school.course"].search_count(
                [("teacher_id", "=", res.id)]
            )
            res.course_count = course_count

    # def _compute_task_count(self):
    #     for res in self:
    #         task_count = self.env["teacher.task"].search_count(
    #             [("teacher_id", "=", res.id)]
    #         )
    #         res.task_count = task_count

    def demo_button(self):
        print("nothing")

    def task_smart_button(self):
        return {
            "name": "Teacher task",
            "res_model": "teacher.task",
            "view_id": False,
            "view_mode": "tree,form",
            #   "domain": [("teacher_id", "=", self.id)],
            "type": "ir.actions.act_window",
        }

    def subject_smart_button(self):
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


# extra details of teacher need to work on
class Teacher_detail(models.Model):
    _name = "teacher.detail"
    _description = "Details on desktop"
