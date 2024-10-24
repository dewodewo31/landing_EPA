from odoo import models, fields

class News(models.Model):
    _name = 'landing.page.news'
    _description = 'Landing Page News'

    title = fields.Char(string='Title', required=True)
    content = fields.Text(string='Content', required=True)
    author_id = fields.Many2one('res.users', string='Author', default=lambda self: self.env.user, required=True)
    publish_date = fields.Date(string='Publish Date', default=fields.Date.today)
    image = fields.Binary(string='Image')
    tags = fields.Many2many('landing.page.news.tag', string='Tags')

class NewsTag(models.Model):
    _name = 'landing.page.news.tag'
    _description = 'News Tags'

    name = fields.Char(string='Tag Name', required=True)
