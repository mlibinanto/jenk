"""
Session and authentication decorators for protecting views
"""

from functools import wraps
from django.shortcuts import redirect, render
from django.utils import timezone
from datetime import timedelta


def session_required(view_func):
    """
    Decorator to require active user session
    Redirects to login if no session found
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user'):
            return redirect('/login')
        
        # Update last activity
        request.session['last_activity'] = timezone.now().isoformat()
        request.session.modified = True
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def session_required_ajax(view_func):
    """
    Decorator for AJAX requests requiring session
    Returns JSON response if not authenticated
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        from django.http import JsonResponse
        
        if not request.session.get('user'):
            return JsonResponse({
                'status': 'error',
                'message': 'Session expired. Please login again.'
            }, status=401)
        
        # Update last activity
        request.session['last_activity'] = timezone.now().isoformat()
        request.session.modified = True
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def get_session_user(request):
    """
    Helper function to get session user information
    Returns dict with user data or None
    """
    if request.session.get('user'):
        return {
            'username': request.session.get('user'),
            'user_id': request.session.get('user_id'),
            'email': request.session.get('user_email'),
            'name': request.session.get('user_name'),
            'role': request.session.get('user_role'),
            'status': request.session.get('user_status'),
            'login_time': request.session.get('login_time'),
            'last_activity': request.session.get('last_activity'),
        }
    return None
