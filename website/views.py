from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

# Create your views here.
def home(request):
    records = Record.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, 'Ok logged In')
            return redirect('home')
        else:
            messages.success(request, 'not good')
            return redirect('home')


    else:
        return render(request, 'home.html', {'records':records})


def logout_user(request):
    logout(request)
    messages.success(request, 'logged out')
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Registered')
            return redirect('home')
        else:
            return render(request, 'register.html', {'form':form})
            
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
            
def user_record(request, pk):

    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'record':record})
    else:
        messages.success(request, 'Login in first')
        return redirect('home')

    
def delete_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        record.delete()
        messages.success(request, f'Deleted Record for {record}')
        return redirect('home')
    else:
        messages.success(request, 'Login in first')
        return redirect('home')

def add_record(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AddRecordForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Added Record')
                return redirect('home')
        else:
            form = AddRecordForm()
            return render(request, 'add_record.html', {'form':form})
    else:
        messages.success(request, 'Login in first')
        return redirect('home')

def update_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        if request.method=='POST':
            form = AddRecordForm(request.POST, instance=record)
            if form.is_valid():
                form.save()
                messages.success(request, 'Updated Record')
                return redirect('home')
        else:
            form = AddRecordForm(instance=record)
            return render(request, 'update_record.html', {'form':form})
    else:
        messages.success(request, 'Login in first')
        return redirect('home')




    
