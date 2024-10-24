from odoo import http
from odoo.http import request

class ServicesPageController(http.Controller):
    @http.route('/servis_page', type='http', auth='public', website=True)
    def servis_page(self, **kwargs):
        # Render the form page template
        return request.render('landing_EPA.servis_page_template', {})