{
    "name": "Website Blog Clean URLs",
    "version": "18.0.1.0.0",
    "depends": ["website", "website_blog"],
    "data": ["views/blog_templates.xml"],
    "post_init_hook": "post_init_create_redirects",  # remova esta linha se não quiser 301 automáticos
    "installable": True,
}
