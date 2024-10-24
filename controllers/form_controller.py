from odoo import http
from odoo.http import request
import base64

class FormPageController(http.Controller):

    @http.route('/form_page', type='http', auth='public', website=True)
    def form_page(self, **kwargs):
        # Render the form page template
        return request.render('landing_EPA.form_page_template', {})
    
    @http.route('/form/submit', type='http', auth='public', website=True, methods=['POST'], csrf=True)
    def submit_form(self, **post):
        # Menerima data dari form
        lead_title = post.get('lead_title', '')
        name = post.get('name', '')
        company_name = post.get('company_name', '')
        email = post.get('email', '')
        phone = post.get('phone', '')
        description = post.get('description', '')

        # Menangani file attachment
        attachment_file = request.httprequest.files.get('attachment')

        # Validasi untuk field penting
        if lead_title and name and email:
            lead_values = {
                'name': lead_title,  # Menjadi judul lead
                'contact_name': name,
                'email_from': email,
                'phone': phone,
                'description': description,
                'partner_name': company_name,  # Menggunakan 'partner_name' untuk nama perusahaan
            }

            # Membuat lead baru di model CRM
            lead = request.env['crm.lead'].create(lead_values)

            # Menangani attachment jika ada file yang diunggah
            if attachment_file:
                attachment_name = attachment_file.filename
                attachment_data = attachment_file.read()
                attachment_base64 = base64.b64encode(attachment_data).decode('utf-8')

                # Membuat attachment di Odoo
                attachment = request.env['ir.attachment'].create({
                    'name': attachment_name,
                    'type': 'binary',
                    'datas': attachment_base64,
                    'res_model': 'crm.lead',
                    'res_id': lead.id,  # Mengaitkan attachment ke lead yang baru dibuat
                    'mimetype': attachment_file.mimetype,
                })

                # Posting attachment ke chatter CRM lead
                lead.message_post(body="Attachment added", attachment_ids=[attachment.id])

            # Redirect ke halaman terima kasih setelah form berhasil di-submit
            return request.redirect('/form_page')

        # Jika ada field penting yang kosong, kembalikan ke halaman form
        return request.redirect('/form_page')
