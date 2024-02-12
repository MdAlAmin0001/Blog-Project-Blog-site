
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from blogapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signuppage/', signuppage, name='signuppage' ),
    path('loginpage/', loginpage, name='loginpage' ),
    path('dashboard/', dashboard, name='dashboard' ),
    path('logoutpage/', logoutpage, name="logoutpage"),
    path('uploadpost/', uploadpost, name="uploadpost"),
    path('post_detail/<str:id>', post_detail, name="post_detail"),
    path('profile/', profile, name="profile"),
    path('profile_update/<str:id>', profile_update, name="profile_update"),
    path('profile_edit/', profile_edit, name="profile_edit"),
    path('deletepost_feed/<str:id>', deletepost_feed, name="deletepost_feed"),
    path('permission_post/', permission_post, name="permission_post"),
    path('permissioned/<str:id>', permissioned, name="permissioned"),
    path('permissioned_denied/<str:id>', permissioned_denied, name="permissioned_denied"),
    path('search_query/', search_query, name="search_query"),
    path('forgetpassword/', forgetpassword, name="forgetpassword"),
    path('changepassword/', changepassword, name="changepassword"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
