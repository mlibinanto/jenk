# Session Management - Quick Reference Card

## 📋 What's Implemented
- ✅ Database-backed session storage
- ✅ 14-day session timeout (configurable)
- ✅ Automatic session propagation across app
- ✅ Security headers (HTTPOnly, SameSite)
- ✅ Session decorators for view protection
- ✅ Activity tracking (login time, last activity)

---

## 🚀 Quick Usage

### Protect a View
```python
from jenk.decorators import session_required, get_session_user

@session_required
def my_view(request):
    user = get_session_user(request)
    return render(request, 'template.html', {'user': user})
```

### In Templates
```html
{% if request.session.user %}
    Welcome {{ request.session.user_name }}!
{% endif %}
```

### Check Session Manually
```python
if request.session.get('user'):
    username = request.session['user']
    user_id = request.session['user_id']
```

---

## 📁 Modified/New Files

| File | Purpose |
|------|---------|
| [jenk/settings.py](jenk/settings.py) | Session configuration (14-day timeout, database backend) |
| [jenk/middleware.py](jenk/middleware.py) | Custom session management middleware |
| [jenk/decorators.py](jenk/decorators.py) | `@session_required`, `@session_required_ajax` decorators |
| [website/views.py](website/views.py) | Enhanced login/logout with full session data |

---

## 📚 Documentation

- [SESSION_SETUP_SUMMARY.md](SESSION_SETUP_SUMMARY.md) - Full implementation overview
- [SESSION_MANAGEMENT_GUIDE.md](SESSION_MANAGEMENT_GUIDE.md) - Detailed configuration & troubleshooting
- [EXAMPLES_SESSION_USAGE.py](EXAMPLES_SESSION_USAGE.py) - 12+ copy-paste code examples

---

## 🔧 Configuration (in settings.py)

```python
SESSION_ENGINE = 'django.contrib.sessions.backends.db'    # Store in database
SESSION_COOKIE_AGE = 1209600                               # 14 days timeout
SESSION_SAVE_EVERY_REQUEST = True                          # Save on every request
SESSION_EXPIRE_AT_BROWSER_CLOSE = False                    # Keep after browser closes
SESSION_COOKIE_HTTPONLY = True                             # Security: no JS access
SESSION_COOKIE_SAMESITE = 'Lax'                            # Security: CSRF protection
```

---

## 💾 Session Data Available

```
session['user']           → username
session['user_id']        → database user ID  
session['user_email']     → user email
session['user_name']      → user full name
session['user_role']      → user role/permission level
session['user_status']    → active/inactive status
session['login_time']     → when user logged in
session['last_activity']  → last activity timestamp
```

---

## ⚙️ First Steps

1. Run migrations: `python manage.py migrate`
2. Test login → creates session ✓
3. Test logout → clears session ✓
4. Check session available in views ✓
5. Use `@session_required` on protected views ✓

---

## 🔐 Security Settings for Production

```python
SESSION_COOKIE_SECURE = True              # Use only with HTTPS
SESSION_COOKIE_HTTPONLY = True            # Already set
CSRF_COOKIE_SECURE = True                 # Use only with HTTPS
CSRF_COOKIE_HTTPONLY = True               # Add this
```

---

## 🐛 Common Checks

**Session not persisting?**
→ Run: `python manage.py migrate` (creates django_session table)

**User keeps getting logged out?**
→ Set `SESSION_COOKIE_AGE` to larger value in settings.py

**Can't access session in templates?**
→ Ensure `{{ request.session.key }}` syntax (not `request.session.key`)

**Session not available in all apps?**
→ ✓ Already configured via middleware

---

## 📊 Active Sessions Management

View active sessions in Django admin:
```
http://yoursite/admin/
→ Navigate to "Sessions"
→ See all active user sessions with expiry dates
```

Or via Django shell:
```bash
python manage.py shell
from django.contrib.sessions.models import Session
from django.utils import timezone
# View active sessions
Session.objects.filter(expire_date__gt=timezone.now())
```

---

## ✨ Key Features Enabled

| Feature | Status |
|---------|--------|
| Session persists across restarts | ✅ Database-backed |
| Session available to all views | ✅ Middleware-enabled |
| Session in AJAX calls | ✅ `@session_required_ajax` |
| Session in templates | ✅ `{{ request.session }}` |
| Automatic activity tracking | ✅ Updated on every request |
| Session timeout | ✅ 14 days (configurable) |
| Security headers | ✅ HTTPOnly, SameSite, Secure(prod) |

---

## 🔗 Session Accessible In

- ✅ Views (any app)
- ✅ Templates 
- ✅ Middleware
- ✅ AJAX endpoints
- ✅ Class-based views
- ✅ API views
- ✅ Signals/Receivers
- ✅ Context processors

---

**Last Updated**: January 25, 2026  
**Status**: Production Ready ✅
