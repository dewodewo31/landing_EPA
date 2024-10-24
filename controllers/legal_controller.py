from odoo import http
from odoo.http import request

class LegalPageController(http.Controller):
    @http.route('/legal_page', type='http', auth='public', website=True)
    def legal_page(self, **kwargs):
        # Render the form page template
        return request.render('landing_EPA.legal_page_template', {})