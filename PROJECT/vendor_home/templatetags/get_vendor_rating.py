from django import template
from vendor_admin.models import States, Vendor_Users
from content_app.models import event_categories
from eventmanager.models import event_heads_manager, event_reviews_user_to_vendor, vendor_event_proposal, vendor_event_proposal_items
register = template.Library()


@register.filter
def getrating(value):
    db = event_reviews_user_to_vendor.objects.filter(vendor_id = value)
    count = db.count()
    if count == 0:

        return 'No Rating'
    else:
        review_list = list(db.values_list('review_star',flat = True))
        count_1=0
        count_2=0
        count_3=0
        count_4=0
        count_5=0
        for i in review_list:
            if int(i) == 1:
                count_1+=1
            if int(i) == 2:
                count_2+=1
            if int(i) == 3:
                count_3+=1
            if int(i) == 4:
                count_4+=1
            if int(i) == 5:
                count_5+=1
        
        avg_rating = ((1*count_1)+(2*count_2)+(3*count_3)+(4*count_4)+(5*count_5))/count
        return round(avg_rating,2)

@register.filter
def getstar(value):
    db = event_reviews_user_to_vendor.objects.filter(vendor_id = value)
    count = db.count()
    if count == 0:
        return count
    else:
        review_list = list(db.values_list('review_star',flat = True))
        count_1=0
        count_2=0
        count_3=0
        count_4=0
        count_5=0
        for i in review_list:
            if int(i) == 1:
                count_1+=1
            if int(i) == 2:
                count_2+=1
            if int(i) == 3:
                count_3+=1
            if int(i) == 4:
                count_4+=1
            if int(i) == 5:
                count_5+=1
        
        avg_rating = ((1*count_1)+(2*count_2)+(3*count_3)+(4*count_4)+(5*count_5))/count
        return int(avg_rating)

@register.filter
def get_rating_count(value):
    db = event_reviews_user_to_vendor.objects.filter(vendor_id = value)
    return db.count()