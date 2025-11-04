from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from .forms import StudentRegistration
from .models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.

# home 
def home(request):
    return render(request, 'myapp/home.html')

# signup view
def user_signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        if User.objects.filter(name=name).exists():
            messages.error(request, "Username already taken.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('signup')

        user = User.objects.create(name=name, email=email, password=password1)
        user.save()
        messages.success(request, "Account created successfully! You can now log in.")
        return redirect('login')
    return render(request, 'myapp/signup.html')

# login 
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome, {user.username}!")
            return redirect('/')  # redirect to home
        else:
            messages.error(request, "Invalid username or password!")
    return render(request, 'myapp/login.html')

# logout view
def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return HttpResponseRedirect('/')

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

    # search_query = request.GET.get('search', '').strip()
    # sort_by = request.GET.get('sort', 'id')
    # order = request.GET.get('order', 'asc')
    # id_min = request.GET.get('id_min')
    # id_max = request.GET.get('id_max')
    search = request.GET.get('search', '').strip()
    id_min = request.GET.get('id_min', '').strip()
    id_max = request.GET.get('id_max', '').strip()
    sort_field = request.GET.get('sort', 'id').strip()
    order = request.GET.get('order', 'asc').strip()
    stud = User.objects.all()

    # # # Keyword filter (by name or email)
    # if search_query:
    #     stud = stud.filter(Q(name__icontains=search_query) | Q(email__icontains=search_query))

    # # # Range filter (ID range)
    # if id_min and id_max:
    #     stud = stud.filter(id__range=(id_min, id_max))
    # elif id_min:
    #     stud = stud.filter(id__gte=id_min)
    # elif id_max:
    #     stud = stud.filter(id__lte=id_max)

    # # # Sorting logic
    # if order == 'desc':
    #     sort_by = f'-{sort_by}'
    # stud = stud.order_by(sort_by)
    
    # Apply text filter
    if search:
        stud = stud.filter(Q(name__icontains=search) | Q(email__icontains=search))

    # Apply ID range
    if id_min and id_max:
        stud = stud.filter(id__range=(id_min, id_max))
    elif id_min:
        stud = stud.filter(id__gte=id_min)
    elif id_max:
        stud = stud.filter(id__lte=id_max)

    # Sorting 
    allowed = ['id', 'name', 'email']
    if sort_field not in allowed:
        sort_field = 'id'
    sort_expression = f'-{sort_field}' if order == 'desc' else sort_field
    stud = stud.order_by(sort_expression)

    # add a pagination 
    # all_post = User.objects.all().order_by('id')
    # paginator = Paginator(all_post, per_page = 4) # Show 4 contacts per page.
    # page_number = request.GET.get('page')
    # stud = paginator.get_page(page_number)
    # print("Page Number:", page_number)
    # print("Page Object:", stud)
    paginator = Paginator(stud, 3)
    page = request.GET.get('page')
    stud = paginator.get_page(page)
    print("Page Number:", page)
    print("Page Object:", stud)

    # Keep querystring for pagination links
    querydict = request.GET.copy()
    querydict.pop('page', None)
    preserved_query = querydict.urlencode()

    # context = {
    #     'form': fm,
    #     'stu': stud,
    #     'search_query': search_query,
    #     'sort_by': sort_by.lstrip('-'),
    #     'order': order,
    #     'id_min': id_min,
    #     'id_max': id_max,
    # }
    context = {
        'form': fm,
        'stu': stud,
        'search': search,
        'id_min': id_min,
        'id_max': id_max,
        'sort_field': sort_field,
        'order': order,
        'preserved_query': preserved_query,
    }
     
    return render(request, 'myapp/addandshow.html', context)

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