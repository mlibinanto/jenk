# Django Session Management Implementation Guide

## Overview
This implementation provides complete session management for your Django application, ensuring user sessions are properly maintained and propagated across the entire application until they expire.

## Configuration Changes Made

### 1. Settings.py (jenk/settings.py)
Added comprehensive session configuration:

```python
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Store sessions in database
SESSION_COOKIE_AGE = 1209600  # 14 days (in seconds)
SESSION_SAVE_EVERY_REQUEST = True  # Save session on every request
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Keep session after browser close
SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to session cookie
SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
SESSION_COOKIE_DOMAIN = None  # Available across domain
SESSION_COOKIE_NAME = 'sessionid'  # Cookie name
```

### 2. Middleware (jenk/middleware.py)
Created custom middleware for session management:

- **SessionManagementMiddleware**: Manages session creation and user activity tracking
- **SessionExpiryMiddleware**: Handles session expiry and cleanup

### 3. Decorators (jenk/decorators.py)
Created helper decorators:

- `@session_required`: Protects views that require authentication
- `@session_required_ajax`: Protects AJAX endpoints requiring authentication
- `get_session_user()`: Helper to retrieve session user data

### 4. Views (website/views.py)
Updated view functions:

- **login()**: Creates comprehensive session with user data
- **logout()**: Properly flushes entire session
- **index()**: Already checks for session, now will work with updated middleware

## Usage Guide

### 1. Using Session Decorators

```python
from jenk.decorators import session_required, session_required_ajax, get_session_user

# For regular views
@session_required
def protected_view(request):
    user_data = get_session_user(request)
    return render(request, 'template.html', {'user': user_data})

# For AJAX views
@session_required_ajax
def api_endpoint(request):
    user_data = get_session_user(request)
    return JsonResponse({'user': user_data})
```

### 2. Manual Session Checks

```python
# Check if user is logged in
if request.session.get('user'):
    username = request.session.get('user')
    user_id = request.session.get('user_id')
    # User is authenticated
else:
    # User is not authenticated
```

### 3. Accessing Session Data in Templates

```html
{% if request.session.user %}
    <p>Welcome, {{ request.session.user }}!</p>
    <p>Email: {{ request.session.user_email }}</p>
    <p>Role: {{ request.session.user_role }}</p>
{% else %}
    <p><a href="/login">Please login</a></p>
{% endif %}
```

## Session Data Structure

When a user logs in, the following data is stored in the session:

```python
{
    'user': 'username',              # Username
    'user_id': 1,                    # User ID
    'user_email': 'user@email.com',  # User email
    'user_name': 'Full Name',        # User full name
    'user_role': 2,                  # User role
    'user_status': 1,                # User status
    'login_time': '2026-01-25T...',  # Login timestamp
    'last_activity': '2026-01-25T...'  # Last activity timestamp
}
```

## Session Configuration Options

### Timeout Settings

Change `SESSION_COOKIE_AGE` in settings.py to adjust timeout:

```python
SESSION_COOKIE_AGE = 3600      # 1 hour
SESSION_COOKIE_AGE = 86400     # 1 day
SESSION_COOKIE_AGE = 604800    # 1 week
SESSION_COOKIE_AGE = 1209600   # 14 days (default)
SESSION_COOKIE_AGE = 2592000   # 30 days
```

### Production Settings

For production with HTTPS:

```python
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
```

## Database Preparation

Ensure session table exists in database:

```bash
python manage.py migrate
```

This creates the `django_session` table which stores all session data.

## Accessing Session Across Application

The session is automatically available in:

1. **All Views**: `request.session`
2. **Templates**: `{{ request.session.user }}`
3. **Middleware**: `request.session`
4. **APIViews**: `request.session`
5. **Class-Based Views**: `self.request.session`

## Important Notes

1. **Session Persistence**: Sessions are stored in database, so they persist across server restarts
2. **Automatic Cleanup**: Django automatically cleans up expired sessions
3. **Session Modification**: Any change to `request.session` is automatically saved due to `SESSION_SAVE_EVERY_REQUEST = True`
4. **CSRF Protection**: Session automatically works with Django's CSRF protection
5. **Security**: HTTPOnly and SameSite flags prevent unauthorized access

## Troubleshooting

### Session not persisting:
- Ensure migrations are applied: `python manage.py migrate`
- Check that `SessionMiddleware` is in MIDDLEWARE list
- Verify `SESSION_ENGINE` is set correctly

### Sessions being cleared immediately:
- Set `SESSION_EXPIRE_AT_BROWSER_CLOSE = False`
- Ensure `SESSION_COOKIE_AGE` is set appropriately
- Check that `SESSION_SAVE_EVERY_REQUEST = True`

### Cannot access session in templates:
- Ensure `request` is passed in context
- Use `{{ request.session.key_name }}` to access session data
- Verify `django.contrib.sessions` is in INSTALLED_APPS

## Example: Complete Protected View

```python
from django.shortcuts import render, redirect
from jenk.decorators import session_required, get_session_user

@session_required
def dashboard(request):
    user_data = get_session_user(request)
    
    # Do something with user data
    context = {
        'user': user_data,
        'page_title': 'Dashboard'
    }
    
    return render(request, 'dashboard.html', context)

def logout_view(request):
    request.session.flush()
    return redirect('/login')
```

## Monitoring Active Sessions

To view active sessions in Django admin:
1. Go to http://yoursite/admin/
2. Navigate to "Sessions" under "Django contrib"
3. See all active sessions with their expiry times
