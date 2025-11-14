from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User as AuthUser
from django.core.paginator import Paginator
from django.db.models import Q
from .models import User
from .forms import StudentRegistration

# HOME
def home(request):
    return render(request, 'myapp/home.html')

# SIGNUP 
def user_signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        if AuthUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        # Check Admin dependency
        if role == "Project Manager" and not User.objects.filter(role='Admin').exists():
            messages.error(request, "Admin must exist before creating a Project Manager.")
            return redirect('signup')
        if role == "Developer" and not User.objects.filter(role='Project Manager').exists():
            messages.error(request, "Project Manager must exist before creating a Developer.")
            return redirect('signup')

        # Create base AuthUser
        auth_user = AuthUser.objects.create_user(username=username, email=email, password=password)
        auth_user.save()

        # Find creator (if logged in)
        creator = None
        if request.user.is_authenticated:
            try:
                creator = User.objects.get(user=request.user)
            except:
                creator = None

        # Create custom role user
        custom_user = User.objects.create(
            user=auth_user,
            name=name,
            email=email,
            password=password,
            role=role,
            created_by=creator
        )

        messages.success(request, f"{role} account created successfully!")
        return redirect('login')

    return render(request, 'myapp/signup.html')

# LOGIN 
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

        # Check hierarchy
        try:
            profile = User.objects.filter(user=user).first()
        except User.DoesNotExist:
            messages.error(request, "No user profile found.")
            return redirect('login')

        if profile.role != "Admin":
            admin_exists = User.objects.filter(role='Admin').exists()
            if not admin_exists:
                messages.error(request, "Admin must log in first before others.")
                return redirect('login')

        login(request, user)
        messages.success(request, f"Welcome {user.username} !")
        return redirect('addandshow')

    return render(request, 'myapp/login.html')

# LOGOUT
def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

# ADD AND SHOW 
def add_show(request):
    current_user = request.user
    try:
        profile = User.objects.get(user=current_user)
        role = profile.role
    except:
        role = None
        profile = None

    # Create new record
    if request.method == 'POST':
        if role not in ['Admin', 'Project Manager']:
            messages.error(request, "You don't have permission to add records.")
            return redirect('addandshow')

        fm = StudentRegistration(request.POST)
        if fm.is_valid():
            instance = fm.save(commit=False)
            instance.created_by = profile
            instance.user = current_user
            instance.save()
            messages.success(request, 'Record added successfully!')
            return redirect('addandshow')
    else:
        fm = StudentRegistration()

    # Filtering based on role
    if role == 'Admin':
        stud = User.objects.all()
    elif role == 'Project Manager':
        stud = User.objects.filter(created_by=profile)
    elif role == 'Developer':
        stud = User.objects.filter(user=current_user)
    else:
        stud = User.objects.none()
        
    # Search, sort, range filter
    search = request.GET.get('search', '')
    id_min = request.GET.get('id_min', '')
    id_max = request.GET.get('id_max', '')
    sort_field = request.GET.get('sort', 'id')
    order = request.GET.get('order', 'asc')

    if search:
        stud = stud.filter(Q(name__icontains=search) | Q(email__icontains=search))

    if id_min and id_max:
        stud = stud.filter(id__range=(id_min, id_max))
    elif id_min:
        stud = stud.filter(id__gte=id_min)
    elif id_max:
        stud = stud.filter(id__lte=id_max)

    allowed = ['id', 'name', 'email', 'role']
    if sort_field not in allowed:
        sort_field = 'id'
    sort_expr = f'-{sort_field}' if order == 'desc' else sort_field
    stud = stud.order_by(sort_expr)

    paginator = Paginator(stud, 5)
    page_number = request.GET.get('page')
    stud = paginator.get_page(page_number)

    querydict = request.GET.copy()
    querydict.pop('page', None)
    preserved_query = querydict.urlencode()

    return render(request, 'myapp/addandshow.html', {
        'form': fm,
        'stu': stud,
        'role': role,
        'search': search,
        'id_min': id_min,
        'id_max': id_max,
        'sort_field': sort_field,
        'order': order,
        'preserved_query': preserved_query
    })

# DELETE
def delete_data(request, id):
    current_user = request.user
    try:
        profile = User.objects.get(user=current_user)
        role = profile.role
    except:
        role = None

    record = get_object_or_404(User, pk=id)

    if role == 'Admin' or (role == 'Project Manager' and record.created_by == profile):
        record.delete()
        messages.success(request, "Record deleted successfully.")
    else:
        messages.error(request, "Permission denied.")
    return redirect('addandshow')

# UPDATE
def update_data(request, id):
    current_user = request.user
    profile = User.objects.filter(user=current_user).first()
    record = get_object_or_404(User, pk=id)

    if profile.role == 'Developer' and record.user != current_user:
        messages.error(request, "You can only edit your own profile.")
        return redirect('addandshow')

    if profile.role == 'Project Manager' and record.created_by != profile:
        messages.error(request, "You can only edit your own developers.")
        return redirect('addandshow')

    if request.method == 'POST':
        fm = StudentRegistration(request.POST, instance=record)
        if fm.is_valid():
            fm.save()
            messages.success(request, "Record updated successfully!")
            return redirect('addandshow')
    else:
        fm = StudentRegistration(instance=record)

    return render(request, 'myapp/update.html', {'form': fm})

# IMAGE UPLOAD
def image_view(request):
    if request.method == 'POST':
        form = StudentRegistration(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('addandshow')  
    else:
        form = StudentRegistration()  
    return render(request, 'myapp/image_form.html', {'form': form})        