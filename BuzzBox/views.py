from django.shortcuts import render , redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .models import Profile , Post , LikePost , FollowersCount
from django.core.exceptions import ValidationError
from itertools import chain


def index(request):
    try:
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)
    except User.DoesNotExist:
        messages.error(request, "User does not exist.")
        return redirect('login')
    except Profile.DoesNotExist:
        messages.error(request, "Profile does not exist.")
        return redirect('profile_create') 
    user_following_list = []
    feed = []

    user_following = FollowersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)
    for username in user_following_list:
        followed_user = get_object_or_404(User, username=username)
        feed_lists =  Post.objects.filter(user=followed_user)
        feed.append(feed_lists)

    feed_list = list(chain(*feed)) 
    feed_list = [post for post in feed_list if post.user != user_object]     
   
    
    return render(request, 'BuzzBox/index.html', {'user_profile': user_profile,  'feed_list': feed_list})

@login_required(login_url='login') 
def settings(request):
    try:
        user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        # Create a new profile for the user if it does not exist
        user_profile = Profile.objects.create(user=request.user, id_user=request.user.id)

    if request.method == 'POST':
        if request.FILES.get('image') is None:
            image = user_profile.profile_img
        else:
            image = request.FILES['image']

        bio = request.POST.get('bio', user_profile.bio)
        location = request.POST.get('location', user_profile.location)

        user_profile.profile_img = image
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()

    # Handle GET request
    return render(request, 'BuzzBox/settings.html', {'user_profile': user_profile})




def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                 
                user_login  = auth.authenticate(username=username, password=password)
                auth.login(request, user_login) 


                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()

                return redirect('settings')  
                
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
    else:
        return render(request, 'BuzzBox/signup.html')
    
def login(request):

    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']


        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')
    else:
     return render(request, 'BuzzBox/login.html')    

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')


@login_required(login_url='login')
def upload(request):
    if request.method == 'POST':
        print("POST request received")
        user = request.user
        image = request.FILES.get('image_upload')
        caption = request.POST.get('caption')

        if image:
            print("Image uploaded")
        if caption:
            print("Caption received")

        # Check if image and caption are present
        if image and caption:
            try:
                new_post = Post.objects.create(user=user, image=image, caption=caption)
                print("Post created:", new_post)
                return redirect('/')
            except ValidationError as e:
                print("Validation error:", e)
            except Exception as e:
                print("Error creating post:", e)
        else:
            print("Image or caption missing")
    
    # Handle GET requests
    return redirect('/')

@login_required(login_url='login')
def like_post(request):

    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id) 
    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()   

    if like_filter ==None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect ('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect ('/')

   
@login_required(login_url='login')
def profile(request, username):
    user_object = get_object_or_404(User, username=username)
    user_profile = get_object_or_404(Profile, user=user_object)
    user_posts = Post.objects.filter(user=user_object)  # Assuming 'user' is a ForeignKey in Post
    user_post_length = len(user_posts)

    follower = request.user.username
    user = username

    if FollowersCount.objects.filter(follower=follower, user=user).exists():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'   

    user_followers = len(FollowersCount.objects.filter(user=username))
    user_following = len(FollowersCount.objects.filter(follower=username)) 

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,

    }
    return render(request, 'BuzzBox/profile.html', context)

@login_required(login_url='login')
def follow(request):
    
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).exists():
          delete_follower = FollowersCount .objects.get(follower=follower, user=user)
          delete_follower.delete()
          return redirect('/profile/'+ user)
        else:
          new_follower = FollowersCount.objects.create(follower=follower, user=user)
          new_follower.save()
        return redirect('/profile/'+ user)

    else:
      return redirect('/')


@login_required(login_url='login')
def search (request):
    return render(request, 'search.html')   