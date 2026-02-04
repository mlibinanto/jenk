from django.shortcuts import redirect, render
from django.http import HttpResponse
from Admin.models import Admin
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import datetime

# Create your views here.
def index(request):
    if request.session.get('user'):
        print("Session exists--------------------------------")
        # print(request.session.get('user'))
        data=[]
        user= request.session.get('user')
        data.append(user)
        # print(data)
        return render(request, 'website/index.html', {'data': data})
    else:
        return redirect('/login')

def about(request):
    return render(request, 'about.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('pass')
        
        try:
            admin = Admin.objects.get(username=username)
            if admin.check_password(password):  # Verify Argon2 hashed password
                # Create comprehensive session data
                request.session['user'] = username
                request.session['user_id'] = admin.id
                request.session['user_email'] = admin.email
                request.session['user_name'] = admin.name
                request.session['user_role'] = admin.role
                request.session['user_status'] = admin.status
                request.session['login_time'] = timezone.now().isoformat()
                
                # Mark session as modified to ensure it's saved
                request.session.modified = True
                
                print(f"User {username} logged in successfully")
                print(f"Session ID: {request.session.session_key}")
                
                return redirect('/')
            else:
                return render(request, 'website/login.html', {'error': 'Invalid credentials'})
        except Admin.DoesNotExist:
            return render(request, 'website/login.html', {'error': 'Invalid credentials'})
    return render(request, 'website/login.html')

def register(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('pass')
        repass = request.POST.get('repass')

        if password != repass:
            return render(request, 'website/register.html', {'error': 'Passwords do not match'})

        # Check if username already exists
        if Admin.objects.filter(username=username).exists():
            return render(request, 'website/register.html', {'error': 'Username already exists'})

        # Check if email already exists
        if Admin.objects.filter(email=email).exists():
            return render(request, 'website/register.html', {'error': 'Email already exists'})

        try:
            admin = Admin(
                name=name,
                username=username,
                email=email,
                phone=phone,
                role=2,
                status=1,
            )
            admin.set_password(password)  # Hash with Argon2
            admin.save()
            return redirect('/login')
        except Exception as e:
            return render(request, 'website/register.html', {'error': f'Registration failed: {str(e)}'})
    return render(request, 'website/register.html')

def logout(request):
    try:
        username = request.session.get('user')
        print(f"User {username} logged out")
        
        # Flush the entire session
        request.session.flush()
        
        return redirect('/login')
    except Exception as e:
        print(f"Logout error: {str(e)}")
        request.session.flush()
    return redirect('/login')