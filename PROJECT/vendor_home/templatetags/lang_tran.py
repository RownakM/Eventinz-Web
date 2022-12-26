from django import template
from vendor_admin.models import States, Vendor_Users
from content_app.models import event_categories
from eventmanager.models import event_heads_manager, vendor_event_proposal, vendor_event_proposal_items
from Language_Control.models import *
register = template.Library()
from googletrans import Translator
translator = Translator()
@register.filter
def transl(value,fr):
    a=''
    t=''
    db = Language_Control.objects.filter(status = 'Enable')
    if fr == 'Yes':
        ex = ['Eventinz, The Most Reliable Event Resource Platform in West Africa.']
        english = list(db.values_list('english_text',flat=True))
        french = list(db.values_list('french_text',flat=True))

   
        

        if value in english:
            get_index = english.index(value)
            a = french[get_index]
            return a
        else:
            a = translator.translate(value,dest='fr')
            t = a.text
            return t
    else:
        return value
    