# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')  # Редирект на список продуктов после регистрации
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})  # Рендеринг правильного шаблона

def verification_required(request):
    return render(request, 'users/verification_required.html')
