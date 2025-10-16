from django.shortcuts import render, HttpResponseRedirect
from .forms import StudentRegistration
from .models import User
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.

# Add and Show Data
def add_show(request):
    # messages.add_message(request, messages.SUCCESS, 'New Student Successfully Saved !')
    if request.method == 'POST':
        fm = StudentRegistration(request.POST)
        if fm.is_valid():
            nm = fm.cleaned_data['name']
            em = fm.cleaned_data['email']
            pw = fm.cleaned_data['password']
            reg = User(name=nm, email=em, password=pw)
            reg.save()
            messages.success(request, 'New Student Successfully Saved !')
            fm = StudentRegistration()
    else:
        fm = StudentRegistration()
    stud = User.objects.all()
    # add a pagination 
    all_post = User.objects.all().order_by('-id')
    paginator = Paginator(all_post, per_page = 4) # Show 5 contacts per page.
    page_number = request.GET.get('page')
    stud = paginator.get_page(page_number)
    print("Page Number:", page_number)
    print("Page Object:", stud)
    return render(request, 'myapp/addandshow.html', {'form':fm , 'stu':stud})

# Delete Data
def delete_data(request, id):
    if request.method == 'POST':
        pi = User.objects.get(pk=id)
        pi.delete()
        return HttpResponseRedirect('/')

# Update Data
def update_data(request, id):
    if request.method == 'POST':
        pi = User.objects.get(pk=id)
        fm = StudentRegistration(request.POST, instance=pi)
        if fm.is_valid():
            fm.save()
    else:
        pi = User.objects.get(pk=id)
        fm = StudentRegistration(instance=pi) 
    return render(request, 'myapp/update.html', {'form':fm})