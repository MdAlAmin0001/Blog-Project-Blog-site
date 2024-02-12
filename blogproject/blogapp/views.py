from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import *
from django.core.mail import send_mail
from django.db.models import Q
import random
from blogproject.settings import EMAIL_HOST_USER




def signuppage(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        display_name=request.POST.get('displayName')
        email=request.POST.get('email')
        password=request.POST.get('password')
        User_type=request.POST.get('userType')
        Profile_Image=request.FILES.get('profilePhoto')
        
        user=Custom_User.objects.create_user(username=username,password=password)
        user.display_name=display_name
        user.email=email
        user.user_type=User_type
        user.profile_image=Profile_Image
        user.save()
        return redirect('loginpage')
    return render(request,"signuppage.html")

def loginpage(request):
    if request.method == 'POST':
        myusername=request.POST.get('username')
        mypassword=request.POST.get('password')
        
        user = authenticate(request, username=myusername, password=mypassword)
        print(user)
        
        if user:
            login(request, user)
            return redirect("dashboard")
    return render(request, "loginpage.html")

def logoutpage(request):
    logout(request)
    return redirect("loginpage")

def dashboard(request):
    post=BlogPost.objects.filter(Permission=True).order_by('-Create_at')
    context={
        'pkey':post
    }
    return render(request,"dashboard.html", context)


def profile(request):
    if request.user.is_authenticated:
        userid = request.user.id
        blogger_instance = Custom_User.objects.get(pk=userid)
        blogger_posts = BlogPost.objects.filter(Created_By=blogger_instance)
    return render(request, "profile.html",{'bp':blogger_posts})

def profile_edit(request):
    if request.method == "POST":
        
        display_name=request.POST.get("display_name")
        email=request.POST.get("email")
        user_type=request.POST.get("user_type")
        profile_image=request.FILES.get("profile_image")
   
        
    
        profile=Custom_User(
            display_name=display_name,
            email=email,
            user_type=user_type,
            profile_image= profile_image,
         
        )
        profile.save()
        return redirect('profile')
    return render(request, 'profile_update.html')

def profile_update(request, id):
    profile=Custom_User.objects.filter(id=id)
    context={
        'proeditkey':profile
    }
    
    return render(request, "profile_update.html",context)

def deletepost_feed(request,id):
    post=BlogPost.objects.filter(id=id)
    
    post.delete()
    
    return redirect("dashboard")



def uploadpost(request):
    if request.method == "POST":
        Post_image=request.FILES.get('postImage')
        Post_title=request.POST.get('postTitle')
        Post_description=request.POST.get('postDescription')
        Create_by=request.user
        
        post=BlogPost(
            Post_Image=Post_image,
            Post_Title=Post_title,
            Post_Description=Post_description,
            Created_By=Create_by
        )
        
        post.save()
        return redirect('dashboard')    
    return render(request, "uploadPost.html")

def post_detail(request,id):
    post = get_object_or_404(BlogPost, id=id)
    post.views += 1  # Increment views when post is viewed
    post.save()
    return render(request, 'post_detail.html', {'post': post})


def permission_post(request):
    post=BlogPost.objects.filter(Permission=False)
    context={
        'pkey':post
    }
    return render(request,"approve_post.html", context)
def permissioned(request,id):
    post=BlogPost.objects.get(id=id)
    post.Permission=True
    post.save()
    
    return redirect('permission_post')

def permissioned_denied(request,id):
    post=BlogPost.objects.get(id=id)
    
    post.delete()
    
    return redirect('permission_post')


def search_query(request):
    if request.method == 'POST':
        query=request.POST.get('search')
        search_post=BlogPost.objects.filter(
            Q(Post_Title__icontains=query) | Q(Post_Description__icontains=query)
        )
    return render(request, 'search_query.html',{'sq':search_post})


def forgetpassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = Custom_User.objects.get(email = email)
        otp = random.randint(111111,999999)
        user.otp_token = otp
        user.save()
        
        sub = f"Your Otp:{otp}"
        msg = f"""Dear User,
        Your OTP is:{otp}. Please keep it secret"""
        from_mail = EMAIL_HOST_USER
        receipent = [email]
        send_mail(
            subject = sub,
            recipient_list=receipent,
            from_email=from_mail,
            message=msg,            
        )
        return render(request, 'changepassword.html',{'email':email})
    return render(request, 'forgetpassword.html')

def changepassword(request):
    if request.method == "POST":
        mail = request.POST.get('email')
        otp = request.POST.get('otp')
        password = request.POST.get('password')
        c_password = request.POST.get('c_password')
        user = Custom_User.objects.get(email = mail)
        if user.otp_token != otp:
            return redirect('forgetpassword')
        if password != c_password:
            return redirect('forgetpassword')
        user.set_password(password)
        
        user.save()
        return redirect('loginpage')
    return render(request, 'changepassword.html')

