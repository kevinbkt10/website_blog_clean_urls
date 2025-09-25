from odoo import api, fields, models
from odoo.tools import slugify

class BlogPost(models.Model):
    _inherit = "blog.post"

    clean_slug = fields.Char(index=True, copy=False)
    clean_url = fields.Char(compute="_compute_clean_url", store=False)

    _sql_constraints = [
        ('clean_slug_uniq_per_website', 'unique(clean_slug, website_id)',
         'Já existe um post com esse slug neste site.'),
    ]

    def _base_slug(self):
        self.ensure_one()
        return slugify(self.name) or "post"

    def _ensure_unique_clean_slug(self, base):
        self.ensure_one()
        slug = base
        i = 2
        while self.sudo().search_count([('clean_slug', '=', slug), ('website_id', '=', self.website_id.id)]):
            slug = f"{base}-{i}"
            i += 1
        return slug

    @api.model_create_multi
    def create(self, vals_list):
        recs = super().create(vals_list)
        for rec, vals in zip(recs, vals_list):
            if not vals.get('clean_slug'):
                rec.clean_slug = rec._ensure_unique_clean_slug(rec._base_slug())
        return recs

    def write(self, vals):
        res = super().write(vals)
        for rec in self:
            if 'name' in vals and not vals.get('clean_slug'):
                base = rec._base_slug()
                if not rec.clean_slug:
                    rec.clean_slug = rec._ensure_unique_clean_slug(base)
        return res

    @api.depends('clean_slug', 'website_id')
    def _compute_clean_url(self):
        for rec in self:
            rec.clean_url = f"/p/{rec.clean_slug}" if rec.clean_slug else False
