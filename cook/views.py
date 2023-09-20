from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from .models import Profile,Recipe
import random
# Create your views here.


def index(request):
    return render(request,"cook/home.html")


def login_view(request):
     if request.method == "POST":
        # Accessing username and password from form data
        username = request.POST["username"]
        password = request.POST["password"]

        # Check if username and password are correct, returning User object if so
        user = authenticate(request, username=username, password=password)

        # If user object is returned, log in and route to index page:
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("profile"))
        # Otherwise, return login page again with new context
        else:
            return render(request, "cook/login.html", {
                "message": "Invalid Credentials"
            })
        
       
    
     return render(request,"cook/login.html")


def profile(request):
    if not request.user.is_authenticated:
        return render(request,"cook/login.html")
    return render(request, "cook/profile.html")



def logout_view(request):
    logout(request)
    return render(request, "cook/login.html", {
                "message": "Logged Out"
            })

def signup_view(request):
     if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already taken.')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken.')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                # You don't need to call user.save() explicitly; it's done by create_user.
                login(request, user)  # Log the user in after registration
                return redirect("settings")
        else:
            messages.error(request, 'Passwords do not match.')

     return render(request, 'cook/signup.html')
    


@login_required(login_url='login')
def settings_view(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        image = request.FILES.get('image', user_profile.profileimg)
        bio = request.POST['bio']
        location = request.POST['location']

        user_profile.profileimg = image
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()

        return redirect("settings")

    return render(request, "cook/setting.html", {'user_profile': user_profile})
def recipe_post(request):
     
     if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        ingredients = request.POST['ingredients']
        instructions = request.POST['instructions']
        image = request.FILES['image']

        recipe = Recipe(
            user=request.user,
            title=title,
            description=description,
            ingredients=ingredients,
            instructions=instructions,
            image=image,
            # Set other fields as needed
        )
        recipe.save()

        return redirect("recipe_list")  # Redirect to the recipe list page

     return render(request, 'cook/post.html')  # Render a form for adding recipes
    
    # cook/views.py



def recipe_list_view(request):
    
    # Retrieve recipes for the logged-in user
    recipes = Recipe.objects.filter(user=request.user)

    context = {
        'recipes': recipes,
    }

    return render(request, 'cook/recipe_list.html', context)
