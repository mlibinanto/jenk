"""
Example usage patterns for session management in the Django application
Copy and paste examples as needed in your views
"""

# ============================================================================
# EXAMPLE 1: Using session_required decorator in views
# ============================================================================

from django.shortcuts import render, redirect
from jenk.decorators import session_required, get_session_user

@session_required
def user_dashboard(request):
    """Protected view that requires active session"""
    user_data = get_session_user(request)
    
    context = {
        'user': user_data,
        'page': 'dashboard'
    }
    return render(request, 'dashboard.html', context)


# ============================================================================
# EXAMPLE 2: Manual session check in view
# ============================================================================

def manual_session_check(request):
    """Example of manual session checking without decorator"""
    if not request.session.get('user'):
        return redirect('/login')
    
    username = request.session.get('user')
    user_email = request.session.get('user_email')
    
    return render(request, 'profile.html', {
        'username': username,
        'email': user_email
    })


# ============================================================================
# EXAMPLE 3: AJAX endpoint with session protection
# ============================================================================

from django.http import JsonResponse
from jenk.decorators import session_required_ajax

@session_required_ajax
def api_get_user_data(request):
    """AJAX endpoint that requires session"""
    user_data = get_session_user(request)
    
    return JsonResponse({
        'status': 'success',
        'user': user_data
    })


# ============================================================================
# EXAMPLE 4: Extending session timeout on user activity
# ============================================================================

from django.utils import timezone

def update_user_activity(request):
    """Update session activity time"""
    if request.session.get('user'):
        request.session['last_activity'] = timezone.now().isoformat()
        request.session.modified = True
    
    return JsonResponse({'status': 'success'})


# ============================================================================
# EXAMPLE 5: Class-based view with session
# ============================================================================

from django.views import View
from django.utils.decorators import method_decorator

class DashboardView(View):
    @method_decorator(session_required)
    def get(self, request):
        """GET request to dashboard"""
        user_data = get_session_user(request)
        return render(request, 'dashboard.html', {'user': user_data})
    
    @method_decorator(session_required)
    def post(self, request):
        """POST request to dashboard"""
        user_data = get_session_user(request)
        # Process form data
        return JsonResponse({'status': 'success', 'user': user_data})


# ============================================================================
# EXAMPLE 6: Using session in context processor (for templates)
# ============================================================================

# In jenk/context_processors.py:
def user_session_context(request):
    """Make session data available in all templates"""
    from jenk.decorators import get_session_user
    
    user_data = get_session_user(request)
    return {
        'user_session': user_data,
        'is_authenticated': bool(user_data)
    }

# Then add to settings.py:
# TEMPLATES = [
#     {
#         'OPTIONS': {
#             'context_processors': [
#                 # ... existing context processors
#                 'jenk.context_processors.user_session_context',
#             ],
#         },
#     },
# ]


# ============================================================================
# EXAMPLE 7: Template usage
# ============================================================================

"""
In your templates:

<!-- Check if user is logged in -->
{% if request.session.user %}
    <p>Welcome, {{ request.session.user }}!</p>
    <p>Email: {{ request.session.user_email }}</p>
    <p>Role: {{ request.session.user_role }}</p>
{% else %}
    <p><a href="/login">Please login</a></p>
{% endif %}

<!-- Or using context processor (if configured) -->
{% if is_authenticated %}
    <p>Welcome, {{ user_session.name }}!</p>
{% endif %}
"""


# ============================================================================
# EXAMPLE 8: Handling session expiry in API calls
# ============================================================================

from django.http import JsonResponse

def handle_session_expiry(view_func):
    """Decorator to handle session expiry in API responses"""
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user'):
            return JsonResponse({
                'status': 'error',
                'message': 'Session expired. Please login again.',
                'redirect': '/login'
            }, status=401)
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


# ============================================================================
# EXAMPLE 9: Multi-app session access
# ============================================================================

# In api/views.py:
from django.http import JsonResponse

def get_collections(request):
    """API view in different app accessing session"""
    if not request.session.get('user'):
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    user_id = request.session.get('user_id')
    # Get collections for this user
    
    return JsonResponse({'collections': []})


# ============================================================================
# EXAMPLE 10: Logout with cleanup
# ============================================================================

def logout_view(request):
    """Properly logout and clear session"""
    username = request.session.get('user')
    
    # Log the logout action if needed
    print(f"User {username} logged out at {timezone.now()}")
    
    # Flush entire session
    request.session.flush()
    
    # Redirect to login
    return redirect('/login')


# ============================================================================
# EXAMPLE 11: Session data in signals/tasks
# ============================================================================

from django.db.models.signals import post_save
from django.dispatch import receiver
from Admin.models import Admin

@receiver(post_save, sender=Admin)
def on_admin_update(sender, instance, **kwargs):
    """Handle admin updates (can be used with session data)"""
    # If needed, you can access user through request context
    # In async tasks, you'll need to pass session data explicitly
    pass


# ============================================================================
# EXAMPLE 12: Middleware-level session access
# ============================================================================

# In jenk/middleware.py:
class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Access session before view
        if request.session.get('user'):
            user = request.session.get('user')
            print(f"Request from: {user}")
        
        response = self.get_response(request)
        
        # Access session after view
        if request.session.get('user'):
            print(f"User session still active: {request.session.get('user')}")
        
        return response
