from django.shortcuts import render
from myapp.models import Student
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Create your views here.

class StudentCreateView(CreateView):
    model = Student
    fields = ['name', 'email', 'roll']
    # template_name = 'myapp/student_form.html' # if you use generic name then no need to specify
    success_url = '/student/'

class StudentListView(ListView):
    model = Student   
    context_object_name = 'students'
  

class StudentDetailView(DetailView):
    model = Student   
    context_object_name = 'student'

class StudentUpdateView(UpdateView):
    model = Student
    fields = ['name', 'email', 'roll']
    success_url = '/student/'
    
class StudentDeleteView(DeleteView):
    model = Student
    success_url = '/student/'