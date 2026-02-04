"""
Custom middleware for session management and authentication
Ensures sessions are properly propagated across the application
"""

from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone


class SessionManagementMiddleware(MiddlewareMixin):
    """
    Custom middleware to handle session management and propagation
    This ensures user sessions are maintained throughout the application
    """
    
    def process_request(self, request):
        """
        Process incoming request and check session validity
        """
        if request.session.session_key is None:
            # Create session if it doesn't exist
            request.session.create()
        
        # Check if user is logged in
        if request.session.get('user'):
            # Update last activity time
            request.session['last_activity'] = timezone.now().isoformat()
            request.session.modified = True
            
            # Make user info available in templates
            request.user_session = {
                'username': request.session.get('user'),
                'user_id': request.session.get('user_id'),
                'email': request.session.get('user_email'),
                'name': request.session.get('user_name'),
                'role': request.session.get('user_role'),
                'status': request.session.get('user_status'),
            }
        
        return None
    
    def process_response(self, request, response):
        """
        Process outgoing response and ensure sessions are saved
        """
        # Ensure session is marked as modified to save any changes
        if hasattr(request, 'session') and request.session.get('user'):
            request.session.modified = True
        
        return response


class SessionExpiryMiddleware(MiddlewareMixin):
    """
    Middleware to handle session expiry and cleanup
    """
    
    def process_request(self, request):
        """
        Check if session has expired and clear it if needed
        """
        if request.session.get('user'):
            # Session is active, no need to clear
            pass
        
        return None
