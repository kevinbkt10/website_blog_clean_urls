from odoo import http
from odoo.http import request

class BlogCleanURL(http.Controller):
    @http.route(['/p/<string:clean_slug>'], type='http', auth='public', website=True, sitemap=True)
    def blog_clean(self, clean_slug, **kw):
        post = request.env['blog.post'].sudo().search([
            ('clean_slug', '=', clean_slug),
            ('website_id', '=', request.website.id),
            ('is_published', '=', True),
        ], limit=1)
        if not post:
            return request.not_found()
        return request.render('website_blog.blog_post', {
            'blog_post': post,
            'main_object': post,
            'blog': post.blog_id,
        })
