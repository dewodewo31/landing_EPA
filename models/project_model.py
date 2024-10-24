from odoo import models, fields

class ProjectProject(models.Model):
    _inherit = 'project.project'

    process = fields.Char(string="Process")
    project_size = fields.Float(string="Project Size (in sq m)")
    years = fields.Char(string="Years")
    location = fields.Char(string="Location")  # Tambahkan field location
