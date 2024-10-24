from odoo import http
from odoo.http import request

class AboutPageController(http.Controller):

    @http.route('/about_page', type='http', auth='public', website=True)
    def about_page(self, **kwargs):
        # Render the form page template
        return request.render('landing_EPA.about_page_template', {})