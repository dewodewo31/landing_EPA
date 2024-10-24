from odoo import http
from odoo.http import request

class LandingPageController(http.Controller):

    @http.route('/landing_page', type='http', auth='public', website=True)
    def landing_page(self, **kwargs):
        # Render the landing page template
        return request.render('landing_EPA.landing_page_template', {})

