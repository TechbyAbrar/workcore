from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import ToDone
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def homepage(request):
    return render(request, 'todoApp/homepage.html')

def signupway(request):
    if request.method == 'POST':
        un = request.POST.get('username')
        em = request.POST.get('email')
        pwd = request.POST.get('password')
        pwd2 = request.POST.get('password2')
        if pwd == pwd2:
            print(un, em, pwd)
            user = User.objects.create_user(username=un, email=em, password=pwd)
            user.save()
            return redirect('login')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('signup')
        
    return render(request, 'todoApp/signup.html')

def loginway(request):
    if request.method == 'POST':
        un = request.POST.get('username')
        pwd = request.POST.get('password')
        print(un, pwd)
        user = authenticate(request, username = un, password = pwd)
        if user is not None:
            login(request, user)
            return redirect('corepage')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')
    return render(request, 'todoApp/login.html')


@login_required  # Protects this view from unauthorized access
def corepage(request):
    if request.method == 'POST':
        title = request.POST.get('task_title', '').strip()

        if not title:
            messages.error(request, "Task title cannot be empty.")
            return redirect('corepage')

        ToDone.objects.create(title=title, user=request.user)
        messages.success(request, "Task added successfully!")
        return redirect('corepage')

    tasks = ToDone.objects.filter(user=request.user).order_by('-date')  # Fetch all tasks in descending order of date

    return render(request, 'todoApp/corepage.html', context={'tasks':tasks})

#update
def task_update(request, sn):
    # Use snake_case for function names (PEP8 standard)
    task = get_object_or_404(ToDone, sn=sn)  # Fetch task or 404 if not found

    if request.method == 'POST':
        task_title = request.POST.get('task_title')
        task_description = request.POST.get('task_description')

        # Only update if the new values are different
        if task_title and task_title != task.title:
            task.title = task_title
        if task_description and task_description != task.description:
            task.description = task_description

        # Save the task only if something changed (this prevents unnecessary DB writes)
        task.save()
        return redirect('corepage') 
    
    context = {'task': task}
    return render(request, 'todoApp/taskUpdate.html', context)

#delete
def delete_task(request, sn):
    task = get_object_or_404(ToDone, sn=sn)  # Fetch task or return 404 if not found
    
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task Deleted Successfully!')
        return redirect('corepage') 
    return render(request, 'todoApp/confirm_delete.html', {'task': task})

#logout
def logout_way(request):
    if request.user.is_authenticated:  # Check if the user is authenticated
        logout(request) 
        return redirect('home') 
    else:
        return redirect('home')