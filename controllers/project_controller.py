import base64
from odoo import http
from odoo.http import request

class ProjectPageController(http.Controller):

    @http.route('/project_page', type='http', auth='public', website=True)
    def project_page(self, **kwargs):
        # Render the form page template
        return request.render('landing_EPA.project_page_template', {})

    @http.route('/input_project', type='http', auth='public', website=True, csrf=False)
    def input_project(self, **kwargs):
        # Menyimpan data dari form ke dalam model project.project
        if request.httprequest.method == 'POST':
            project_name = kwargs.get('name')
            company_name = kwargs.get('company_name')
            location = kwargs.get('location')
            process = kwargs.get('process')
            project_size = kwargs.get('project_size')
            years = kwargs.get('years')
            description = kwargs.get('custom_description')  # Field baru untuk deskripsi
            attachment = request.httprequest.files.get('attachment')  # Mengambil file lampiran

            # Mencari atau membuat partner berdasarkan company_name
            partner = request.env['res.partner'].search([('name', '=', company_name)], limit=1)
            if not partner:
                partner = request.env['res.partner'].create({'name': company_name})

            # Membuat record baru di model project.project
            new_project = request.env['project.project'].create({
                'name': project_name,           # Nama proyek
                'partner_id': partner.id,       # ID partner
                'description': description,     # Field baru untuk deskripsi proyek
                'process': process,             # Field kustom untuk proses
                'project_size': project_size,   # Field kustom untuk ukuran proyek
                'years': years,                 # Field kustom untuk tahun
                'location': location            # Field baru untuk lokasi
            })

            # Jika ada attachment, simpan ke ir.attachment
            if attachment:
                attachment_data = attachment.read()  # Membaca file sebagai bytes
                encoded_attachment = base64.b64encode(attachment_data).decode('utf-8')  # Encode file menjadi base64

                request.env['ir.attachment'].create({
                    'name': attachment.filename,
                    'res_model': 'project.project',
                    'res_id': new_project.id,
                    'datas': encoded_attachment,  # Menyimpan data file yang di-encode
                    'mimetype': attachment.content_type,  # Tipe MIME dari file
                })

            # Redirect atau memberi tahu pengguna setelah berhasil menyimpan
            return request.redirect('/input_project')  # Ganti dengan URL yang sesuai

        # Render template jika bukan POST
        return request.render('landing_EPA.input_project_template', {})
