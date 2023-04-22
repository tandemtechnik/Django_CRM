from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record


# Create your views here.
def home(request):
  records = Record.objects.all()
  # check to see if logged in
  if request.method == "POST":
    username = request.POST['username']
    password = request.POST['password']
    # Authenticate
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      messages.success(request, "You have been logged in")
      return redirect('home')
    else:
      messages.success(request, "There was an error, cannot log in")
      return redirect('home')
  else:
    return render(request, 'crmapp/home.html', {'records': records})

# def login_user(request):
#   pass

def logout_user(request):
  logout(request)
  messages.success(request, "You have been logged out!")
  return redirect('home')

def register_user(request):
  if request.method == "POST":
    form = SignUpForm(request.POST)
    if form.is_valid():
      form.save()
      # Authenticate and Log in
      username = form.cleaned_data['username']
      password = form.cleaned_data['password1']
      user = authenticate(username=username, password=password)
      login(request, user)
      messages.success(request, "You Have Successfully Registered!")
      return redirect('home')  
  else:
    form = SignUpForm() 
    return render(request, 'crmapp/register.html', {'form': form})
  return render(request, 'crmapp/register.html', {'form': form})

def customer_record(request, pk):
  if request.user.is_authenticated:
    # Only Authenticated users can look up records based on id from db
    customer_record = Record.objects.get(id=pk)
    return render(request, 'crmapp/record.html', {'customer_record': customer_record})
  else:
    messages.success(request, "You must be logged in to view records!")
    return redirect('home')
  
  
def delete_record(request, pk):
  if request.user.is_authenticated:
    delete_it = Record.objects.get(id=pk)
    delete_it.delete()
    messages.success(request, "Record Deleted Successfully!")
    return redirect('home')
  else:
    messages.success(request, "You must be logged in to delete records!")
    return redirect('home')
    
    
def add_record(request):
  form = AddRecordForm(request.POST or None)
  if request.user.is_authenticated:
    if request.method =='POST':
      if form.is_valid():
        form.save()
        messages.success(request, "Record Added Successfully!")
        return redirect('home')
  
    return render(request, 'crmapp/add_record.html', {'form': form})
  else:
    messages.success(request, "You must be logged in to add records!")
    return redirect('home')
  
  
def update_record(request, pk):
  if request.user.is_authenticated:
    current_record = Record.objects.get(id=pk)
    form = AddRecordForm(request.POST or None, instance=current_record)
    if form.is_valid():
      form.save()
      messages.success(request, "Record Updated Successfully!")
      return redirect('home')
    return render(request, 'crmapp/update_record.html', {'form': form})
  else:
      messages.success(request, "You must be logged in to update records!")
      return redirect('home')
  
  