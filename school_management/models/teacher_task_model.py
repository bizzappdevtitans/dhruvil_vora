from odoo import fields, models, api
from odoo.exceptions import ValidationError


class SchoolTeacher_Task(models.Model):
    _name = "teacher.task"
    _description = "Details of Task of teacher"
    task_teacher_name = fields.Char(string="Teacher name")
    task_teacher_course = fields.Char(string="Course")
    description_of_task = fields.Char(string="Description")
