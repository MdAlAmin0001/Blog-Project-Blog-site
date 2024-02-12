from django.contrib import admin

from .models import *

class Custom_User_Display(admin.ModelAdmin):
    list_display=['display_name','email','user_type']
    
class BlogPost_Display(admin.ModelAdmin):
    list_display=['Created_By','Post_Title','Create_at']
    
admin.site.register(Custom_User,Custom_User_Display)
admin.site.register(BlogPost,BlogPost_Display)