from django.contrib import messages  
from django.contrib.auth import authenticate, login , logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.decorators import login_required

@login_required
def recipee(request):

    if request.method == 'POST':
        data = request.POST
        
        recipe_name = data.get('recipe_name') 
        recipe_discription = data.get('recipe_discription')
        recipe_image = request.FILES.get('recipe_image')

        recipe.objects.create(
            recipe_name=recipe_name,
            recipe_discription=recipe_discription,
            recipe_image=recipe_image
        )
        
        return redirect('/recipe/') 
    queryset = recipe.objects.all()  
    context = {'recipes': queryset}

    return render(request, 'receipes.html', context)

def delete_recipe(request, recipe_id):
    quaryset = recipe.objects.get(id=recipe_id) 
    quaryset.delete()  
    return redirect('/recipe/')

def update_recipe(requst,recipe_id):
   quaryset = recipe.objects.get(id=recipe_id) 
   if requst.method == 'POST':
       data = requst.POST
       recipe_name = data.get('recipe_name')
       recipe_discription = data.get('recipe_discription')
       recipe_image = requst.FILES.get('recipe_image')
       quaryset.recipe_name = recipe_name
       quaryset.recipe_discription = recipe_discription
       if recipe_image:
            quaryset.recipe_image = recipe_image
       quaryset.save()  
       messages.info(requst, "account created sucsessfuly")
       return redirect('/recipe/')  
   context = {'recipe': quaryset}
   return render(requst,'update_recipe.html',context)

def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # 1. Use the exact username from your QuerySet
        user_obj = User.objects.filter(username=email).first()

        if user_obj is None:
            messages.error(request, "Invalid Email")
            return redirect('/login/')
        
        # 2. FIX: Add 'request' as the first positional argument
        user = authenticate(request, username=email, password=password)
       
        if user is not None:
            login(request, user)
            return redirect('/recipe/')
        else:
            # If user_obj exists but authenticate is None, the password is wrong
            messages.error(request, "Invalid Password")
            return redirect('/login/')
        
    return render(request, 'login.html')


def logout_page(requst):
    logout(requst)
    return redirect('/login/')

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username=email).exists():
            messages.info(request, "Email already taken")
            return redirect('/register/')

        # Create the user
        user = User.objects.create_user(
            username=email, # Using email as username
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.save()
        
        # Redirect to login or home after successful registration
        return redirect('/login/') 

    return render(request, 'register.html')