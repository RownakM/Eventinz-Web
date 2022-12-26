from django.contrib import admin

# Register your models here.

from vendor_CMS.models import *

admin.site.register(vendor_header)
admin.site.register(vendor_leads_CMS_main)
admin.site.register(vendor_leads_Steps)
admin.site.register(vendor_category_CMS)
admin.site.register(vendor_testimonials)
admin.site.register(our_clients)
admin.site.register(our_clients_CMS)
admin.site.register(vendor_get_started)

