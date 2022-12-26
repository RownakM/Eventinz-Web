from django.db import models
from tinymce.models import HTMLField
# Create your models here.
class EV_About(models.Model):
    Header_Text=models.CharField(max_length=300)
    Header_subtext=models.CharField(max_length=300)
    Header_Background=models.ImageField(upload_to='eventinz_about/')
    Who_We_Are_Heading=models.CharField(max_length=300)
    Who_We_Are_Sub_Heading=HTMLField()
    Who_We_Are_Image=models.ImageField(upload_to='eventinz_about/Who_We_are')
    Mission_Text=models.CharField(max_length=300)
    Mission_Sub_Text=models.CharField(max_length=4000)
    Eventinz_Teams_Header=models.CharField(max_length=400)

    class Meta:
        verbose_name_plural = 'Eventinz About'

CHOICES={
    ('AWS','AWS'),
    ('LINUX','LINUX'),
    ('IBM','IBM'),
    ('HP','HP'),
    ('Others','Others')
}
class Eventinz_Teams(models.Model):

    profile_image=models.ImageField(upload_to='ev_teams/profile_pic/')
    Full_Name=models.CharField(max_length=400)
    Designation=models.CharField(max_length=5000)
    linkedin_url=models.URLField(blank=True,null=True)
    certification_logo_1=models.ImageField(upload_to='ev_teams/profile/user_certification/',blank=True,null=True)
    certification_link_1=models.URLField(blank=True,null=True)
    certification_logo_2=models.ImageField(upload_to='ev_teams/profile/user_certification/',blank=True,null=True)
    certification_link_2=models.URLField(blank=True,null=True)
    certification_logo_3=models.ImageField(upload_to='ev_teams/profile/user_certification/',blank=True,null=True)
    certification_link_3=models.URLField(blank=True,null=True)
    certification_logo_4=models.ImageField(upload_to='ev_teams/profile/user_certification/',blank=True,null=True)
    certification_link_4=models.URLField(blank=True,null=True)
    certification_logo_5=models.ImageField(upload_to='ev_teams/profile/user_certification/',blank=True,null=True)
    certification_link_5=models.URLField(blank=True,null=True)
    certification_logo_6=models.ImageField(upload_to='ev_teams/profile/user_certification/',blank=True,null=True)
    certification_link_6=models.URLField(blank=True,null=True)
    certification_logo_7=models.ImageField(upload_to='ev_teams/profile/user_certification/',blank=True,null=True)
    certification_link_7=models.URLField(blank=True,null=True)
    certification_logo_8=models.ImageField(upload_to='ev_teams/profile/user_certification/',blank=True,null=True)
    certification_link_8=models.URLField(blank=True,null=True)

    class Meta:
        verbose_name_plural = 'Eventinz Teams'



class EV_About_french(models.Model):
    Header_Text=models.CharField(max_length=300)
    Header_subtext=models.CharField(max_length=300)
    Header_Background=models.ImageField(upload_to='eventinz_about/')
    Who_We_Are_Heading=models.CharField(max_length=300)
    Who_We_Are_Sub_Heading=HTMLField()
    Who_We_Are_Image=models.ImageField(upload_to='eventinz_about/Who_We_are')
    Mission_Text=models.CharField(max_length=300)
    Mission_Sub_Text=models.CharField(max_length=4000)
    Eventinz_Teams_Header=models.CharField(max_length=400)

CHOICES={
    ('AWS','AWS'),
    ('LINUX','LINUX'),
    ('IBM','IBM'),
    ('HP','HP'),
    ('Others','Others')
}
class Eventinz_Teams_french(models.Model):

    profile_image=models.ImageField(upload_to='ev_teams/profile_pic/')
    Full_Name=models.CharField(max_length=400)
    Designation=models.CharField(max_length=5000)
    linkedin_url=models.URLField(blank=True,null=True)
    certification_logo_1=models.ImageField(upload_to='ev_teams/profile/user_certification/',blank=True,null=True)
    certification_link_1=models.URLField(blank=True,null=True)
    certification_logo_2=models.ImageField(upload_to='ev_teams/profile/user_certification/',blank=True,null=True)
    certification_link_2=models.URLField(blank=True,null=True)
    certification_logo_3=models.ImageField(upload_to='ev_teams/profile/user_certification/',blank=True,null=True)
    certification_link_3=models.URLField(blank=True,null=True)
    certification_logo_4=models.ImageField(upload_to='ev_teams/profile/user_certification/',blank=True,null=True)
    certification_link_4=models.URLField(blank=True,null=True)
    certification_logo_5=models.ImageField(upload_to='ev_teams/profile/user_certification/',blank=True,null=True)
    certification_link_5=models.URLField(blank=True,null=True)
    certification_logo_6=models.ImageField(upload_to='ev_teams/profile/user_certification/',blank=True,null=True)
    certification_link_6=models.URLField(blank=True,null=True)
    certification_logo_7=models.ImageField(upload_to='ev_teams/profile/user_certification/',blank=True,null=True)
    certification_link_7=models.URLField(blank=True,null=True)
    certification_logo_8=models.ImageField(upload_to='ev_teams/profile/user_certification/',blank=True,null=True)
    certification_link_8=models.URLField(blank=True,null=True)
