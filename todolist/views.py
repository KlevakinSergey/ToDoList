from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .forms import *
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Task
from django.contrib.auth import get_user_model

User = get_user_model()


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request,
                          'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        return render(request, 'registration/register.html', {'user_form': user_form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse('Authenticated successfully')

            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid login')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})



@login_required
def index(request):
    search_query = request.GET.get('search', '')
    tasks = Task.objects.filter(user=request.user.pk)
    if search_query:
        tasks = Task.objects.filter(title__icontains=search_query)
    paginator = Paginator(tasks, 3)
    page_number = request.GET.get('page',range(1,5))
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = f'?page={page.previous_page_number()}'
    else:
        prev_url = ''
    if page.has_next():
        next_url = f'?page={page.next_page_number()}'
    else:
        next_url = ''

    form = TaskForm
    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            my_user = User.objects.get(id=request.user.id)
            task = form.save(commit=False)
            task.user = my_user
            task.save()

        return redirect('list')
    return render(request, 'index.html', {'tasks': page,'is_paginated': is_paginated, 'form': form, 'prev_url': prev_url, 'next_url': next_url, 'section': 'dashboard'})





def update_task(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            my_user = User.objects.get(id=request.user.id)
            task = form.save(commit=False)
            task.user = my_user
            task.save()
            return redirect('list')


    return  render(request, index(), {'form': form, 'task': task})



def delete_task(request, pk):
    item = Task.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('list')
    return render(request, index(), {'item': item})