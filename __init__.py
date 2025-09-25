from . import models
from . import controllers

# Opcional: cria 301 dos URLs antigos -> novos após instalar
def post_init_create_redirects(cr, registry):
    from odoo.api import Environment, SUPERUSER_ID
    env = Environment(cr, SUPERUSER_ID, {})
    Redirect = env['website.redirect'].sudo()
    for p in env['blog.post'].sudo().search([]):
        if p.clean_slug:
            old = f"/blog/{p.slug}-{p.id}"
            new = f"/p/{p.clean_slug}"
            if not Redirect.search([('website_id', '=', p.website_id.id), ('url_from', '=', old)], limit=1):
                Redirect.create({'website_id': p.website_id.id, 'url_from': old, 'url_to': new, 'type': '301'})
