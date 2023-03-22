# from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .files import NewUserForm, LoginForm,  CreateTask
from crispy_forms.helper import FormHelper

from .models import Task


# from django.contrib.auth.mixins import LoginRequiredMixin


def IndexView(request):
    return render(request, 'index.html')


@login_required(login_url='my_login')
def dashboard(request):
    return render(request, 'profile/dashboard.html')


# the logic for the registration of a user for the task manager
def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("taskapp:login")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = NewUserForm()

    # Use the Crispy Forms helper to add Bootstrap styling to the form
    helper = FormHelper()
    helper.form_class = 'form-group'
    helper.label_class = 'form-label'
    helper.field_class = 'form-control'
    form.helper = helper

    return render(request=request, template_name="register.html", context={"form": form})


# this view is the logic for logging in
def login_request(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('taskapp:dashboard')
    else:
        form = LoginForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


def logout_view(request):
    logout(request)
    return redirect('taskapp:IndexView')


# creating task
login_required(login_url='my-login')


def createTask(request):
    form = CreateTask
    if request.method == 'POST':
        form = CreateTask(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('taskapp:viewTask')

    context = {'form': form}
    return render(request, 'profile/create_task.html', context=context)


@login_required(login_url='my_login')
def viewTask(request):
    current_user = request.user.id
    task = Task.objects.all().filter(user=current_user)
    context = {'task': task}
    return render(request, 'profile/viewtask.html', context=context)


@login_required(login_url='my_login')
def deleteTask(request, pk):
    # we are fetching our tasks from the database with the primary key
    task = Task.objects.get(id=pk)
    if request.method == 'POST':
        # if selected operation then we delete
        task.delete()
        # if deleted then we would like to go to view task
        return redirect('taskapp:viewTask')

    context = {'task': task}
    return render(request, 'profile/delete.html', context=context)


@login_required(login_url='my_login')
def update_task(request, pk):
    task = Task.objects.get(id=pk)
    # this allows us to work on the specific instance of the task (code below)
    form = CreateTask(instance=task)
    if request.method == 'POST':
        form = CreateTask(request.POST, instance=task)
        # if the item is valid then we update the database
        if form.is_valid():
            form.save()
            # then we return the views tasks to see if our database is updated
            return redirect('taskapp:viewTask')

    context = {'form': form, 'task': task}
    return render(request, 'profile/update.html', context=context)

