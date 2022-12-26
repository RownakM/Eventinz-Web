
from django.db import models
import uuid
from tinymce.models import HTMLField


# Create your models here.
from django.contrib.auth.models import User
from image_cropping import ImageRatioField

from vendor_admin.models import vendor_categories


STATUS=(
    (0,'Draft'),
    (1,'Publish')
)
uuid_id=uuid.uuid4()
class blog_category(models.Model):
    category_img=models.ImageField(upload_to='main_site/blog/categories/img')
    category_name=models.CharField(max_length=300)
    vendor_category=models.ForeignKey(vendor_categories,on_delete=models.CASCADE)
    def __str__(self):
        return self.category_name
    class Meta:
        verbose_name_plural = "Blog Categories"
class Post(models.Model):
    blog_id=models.CharField(unique=True,editable=False,default=uuid.uuid4(),max_length=400)
    cover_image=models.ImageField(upload_to="main_site/blog/thumbnail_images")
    title=models.CharField(max_length=200,unique=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    content=HTMLField()
    created_on=models.DateField(auto_now_add=True)
    created_time=models.TimeField(auto_now_add=True)
    category=models.ForeignKey(blog_category,on_delete=models.CASCADE)
    status=models.IntegerField(choices=STATUS,default=0)
    
    
    # image=models.FileField(blank=True)
    def __str__(self):
        return self.title

class PostImage(models.Model):
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
    images = models.ImageField(upload_to = 'main_site/blog/content_images')
    cropping = ImageRatioField('image', '100x100')

 
    def __str__(self):
        return self.post.title

class Blog_CMS(models.Model):
    Title_Image=models.ImageField(upload_to='main_site/blog/cms/img')
    Title=models.CharField(max_length=100)
    category_heading=models.CharField(max_length=200)
    category_sub_heading=models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = 'Blog Header Management'


class Blog_Category_Details(models.Model):
    category=models.ForeignKey(blog_category,on_delete=models.CASCADE)
    cover_image=models.ImageField(upload_to="main_site/blog/category_images/coverimage/")
    Heading=models.CharField(max_length=3000)
    description=HTMLField()

    class Meta:
        verbose_name_plural = 'Blogs Category Details'


