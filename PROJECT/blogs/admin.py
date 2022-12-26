from import_export.admin import ImportExportModelAdmin
from admin_totals.admin import ModelAdminTotals
from django.db.models.functions import Coalesce
from django.db.models import Sum, Avg
from currency_symbols import CurrencySymbols
from numerize import numerize
from django.contrib import admin
from django.utils.safestring import mark_safe


from import_export import resources

# Register your models here.

# Register your models here.
from blogs.models import *

@admin.action(description='Publish Selected Posts')
def make_published(modeladmin, request, queryset):
    queryset.update(status=1)

@admin.action(description='Draft Selected Posts')
def make_draft(modeladmin, request, queryset):
    queryset.update(status=0)
class Post_settings(ImportExportModelAdmin,admin.ModelAdmin):
    readonly_fields=['blog_id']
    list_display=['blog_id','title','category','author','created_on','created_time','status','Action']
    list_display_links=['Action']
    list_per_page=5
    list_filter = ['category']
    actions=[make_published,make_draft]
    
    def Action(self,obj):
        return 'Change'
    
class PostImageAdmin(admin.StackedInline):
    model = PostImage

class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageAdmin]
 
    class Meta:
       model = Post
       
class PostImageAdmin(admin.ModelAdmin):
    pass

class blogcategory_custom(ImportExportModelAdmin,admin.ModelAdmin):
    list_display=['category_name','category_img','vendor_category','Action']
    search_fields=['category_name']
    list_display_links=['Action']
    list_per_page=5

     
    def Action(self,obj):
        return 'Change'
    
   

class BlogCMS_custom(admin.ModelAdmin):
    list_display=['Title','category_heading','category_sub_heading','Action']
    search_fields=['Title','category_heading','category_sub_heading']
    list_display_links=['Action']
    list_per_page=5
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request , obj=None):
        return False
    def Action(self,obj):
        return 'Change'

    
admin.site.register(Post,Post_settings)
admin.site.register(blog_category,blogcategory_custom)
admin.site.register(Blog_CMS,BlogCMS_custom)

class Blog_Category_List(admin.ModelAdmin):
    list_display = ['category','Heading','Description','Edit']
    list_display_links = ['Edit']
    
    def Description(self,obj):
        return mark_safe(obj.description)
    def Edit(self,obj):
        return 'Edit'
    

admin.site.register(Blog_Category_Details,Blog_Category_List)