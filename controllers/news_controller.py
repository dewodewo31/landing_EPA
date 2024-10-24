from odoo import http
from odoo.http import request
import re

class NewsController(http.Controller):
    @http.route('/news_page', auth='public', website=True)
    def news_page(self, page=1, q=None, **kwargs):
        # Pastikan page adalah integer
        try:
            page = int(page)
        except (ValueError, TypeError):
            page = 1  # Jika tidak valid, set ke 1

        domain = []
        if q:
            domain = ['|', ('name', 'ilike', q), ('content', 'ilike', q)]

        # Ambil jumlah total berita yang sesuai dengan pencarian
        total_posts = request.env['blog.post'].search_count(domain)  # Total berita
        limit = 6  # Jumlah berita per halaman
        offset = (page - 1) * limit  # Hitung offset

        # Hitung total halaman
        total_pages = (total_posts + limit - 1) // limit

        # Pastikan page tidak melebihi total pages
        if page < 1:
            page = 1
        elif page > total_pages:
            page = total_pages

        # Ambil data berita dengan limit dan offset
        news_posts = request.env['blog.post'].search(domain, limit=limit, offset=offset)

        # Siapkan list untuk menyimpan data
        news_data = []
        
        # Ekstrak URL gambar dari cover_properties
        for post in news_posts:
            cover_image_match = re.search(r'url\((.*?)\)', post.cover_properties)
            cover_image_url = cover_image_match.group(1).strip('\"') if cover_image_match else '/landing_EPA/static/src/img/default-image.png'
            news_data.append({
                'id': post.id,
                'name': post.name,
                'content': post.content,
                'create_date': post.create_date,
                'cover_image_url': cover_image_url,
            })

        # Kembalikan template dengan data berita dan pagination
        return request.render('landing_EPA.news_page_template', {
            'news_posts': news_data,
            'total_pages': total_pages,
            'current_page': page,
            'search_query': q or '',  # Tambahkan query pencarian ke dalam konteks
        })
