import sae
from grab_ticket import wsgi

sae.add_vendor_dir('vendor')

application = sae.create_wsgi_app(wsgi.application)