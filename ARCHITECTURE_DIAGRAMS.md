# Session Management Architecture Diagram

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER'S BROWSER                              │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  HTTP Request → Django App                              │   │
│  │  Cookie: sessionid=abc123xyz                            │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                    HTTP Request Handler
                               │
         ┌─────────────────────┴─────────────────────┐
         │                                           │
    ┌────▼──────────────────┐         ┌─────────────▼────────┐
    │  DJANGO MIDDLEWARE   │         │  SESSION MIDDLEWARE  │
    │  Stack Processing    │         │  (Custom)            │
    │                      │         │                      │
    │ 1. Security         │         │ ✓ Create if missing  │
    │ 2. Sessions ◄────────────────►│ ✓ Load from DB       │
    │ 3. CSRF             │         │ ✓ Update activity    │
    │ 4. Auth             │         │ ✓ Make available     │
    │ 5. Messages         │         │                      │
    │ 6. Custom ◄─────────────────►│ (SessionManagement   │
    │    Middleware       │         │  + SessionExpiry)    │
    └────┬──────────────────┘       └─────────┬────────────┘
         │                                    │
         │                 ┌──────────────────┘
         │                 │
    ┌────▼─────────────────▼──────────────────┐
    │  request.session Available in View       │
    │  ◄─── Session Data from Database        │
    │                                          │
    │  {                                       │
    │    'user': 'username',                  │
    │    'user_id': 1,                        │
    │    'user_email': 'user@email.com',      │
    │    'user_name': 'Full Name',            │
    │    'user_role': 2,                      │
    │    'user_status': 1,                    │
    │    'login_time': 'ISO timestamp',       │
    │    'last_activity': 'ISO timestamp'     │
    │  }                                       │
    └────┬────────────────┬──────────────────┘
         │                │
         │                │  Can use:
         │                │  @session_required
         │                │  get_session_user(request)
         │                │  request.session.get('user')
         │                │
    ┌────▼────────────────▼──────────────────┐
    │      VIEW/CONTROLLER                    │
    │                                          │
    │  @session_required                      │
    │  def my_view(request):                 │
    │      user = get_session_user(request)  │
    │      return render(request, ...)       │
    └────┬──────────────────┬──────────────────┘
         │                  │
    ┌────▼──────────────┐   │
    │  Protected View   │   │
    │  Access Allowed ✓ │   │
    └─────────────────┘    │
                           │
                      ┌────▼────────────────────────────┐
                      │  RESPONSE                       │
                      │  - Rendered HTML/JSON           │
                      │  - Session ID in Cookie         │
                      │  - CSRF Token                   │
                      │  - User Data in Context         │
                      └────┬─────────────────────────────┘
                           │
                ┌──────────┴────────────┐
                │                       │
         ┌──────▼──────┐         ┌──────▼──────────┐
         │  Database   │         │  User's Browser │
         │  (MySQL)    │         │                 │
         │             │         │ Stores Cookie   │
         │  Session    │         │ sessionid=...   │
         │  Table      │         │                 │
         │  ─────────  │         │ Auto-sends with │
         │  session_id │         │ Every Request   │
         │  session..  │         │                 │
         │  expires..  │         │                 │
         │             │         └─────────────────┘
         └─────────────┘
                 ▲
                 │ Middleware reads/writes
                 │ session on every request
                 │
         ┌───────┴───────┐
         │   Updates:    │
         │ - last_activity
         │ - data changes
         │ - on persist
         │   (SESSION_   │
         │    SAVE_EVERY_
         │    REQUEST)   │
         └───────────────┘
```

## Login Flow

```
┌──────────────┐
│ User Types   │
│ Credentials  │
└──────┬───────┘
       │ POST /login
       │ email + password
       │
   ┌───▼──────────────────────┐
   │  login() View            │
   │                          │
   │  1. Get email/password   │
   │  2. Query Admin table    │
   │  3. Verify password      │
   └───┬──────────────────────┘
       │
       ├─ Password Match? ─ NO ──┐
       │                         │
       │ YES                  ┌──▼──────────────┐
       │                      │ Render login    │
       │                      │ error: "Invalid"│
       │                      └─────────────────┘
       │
   ┌───▼──────────────────────────────────┐
   │  Create Session                      │
   │  ─────────────────────────────────   │
   │  session['user'] = username          │
   │  session['user_id'] = admin.id       │
   │  session['user_email'] = admin.email │
   │  session['user_name'] = admin.name   │
   │  session['user_role'] = admin.role   │
   │  session['user_status'] = admin.st.. │
   │  session['login_time'] = now()       │
   │  session.modified = True             │
   └───┬──────────────────────────────────┘
       │
   ┌───▼────────────────────────────┐
   │  Save to Database              │
   │  (django_session table)        │
   │  - session_key (generated)     │
   │  - session_data (serialized)   │
   │  - expire_date (+14 days)      │
   └───┬────────────────────────────┘
       │
   ┌───▼────────────────────────────┐
   │  Send HTTP Response            │
   │  - Set-Cookie: sessionid=...   │
   │  - Redirect to /               │
   └───┬────────────────────────────┘
       │
   ┌───▼────────────────┐
   │ User's Browser     │
   │ Stores Cookie      │
   │ sessionid=abc123.. │
   └────────────────────┘
```

## Logout Flow

```
┌──────────────┐
│ User Clicks  │
│ Logout       │
└──────┬───────┘
       │ GET /logout
       │
   ┌───▼──────────────────────┐
   │  logout() View           │
   │                          │
   │  1. Get username from    │
   │     session['user']      │
   │  2. Log the logout       │
   │  3. Flush entire session │
   │     request.session      │
   │     .flush()             │
   └───┬──────────────────────┘
       │
   ┌───▼──────────────────────┐
   │  Delete from Database    │
   │  (django_session table)  │
   │  - Remove session_key    │
   │  - Remove all data       │
   │  - Mark expired          │
   └───┬──────────────────────┘
       │
   ┌───▼────────────────────────────┐
   │  Send HTTP Response            │
   │  - Clear-Cookie: sessionid     │
   │  - Redirect to /login          │
   └───┬────────────────────────────┘
       │
   ┌───▼────────────────┐
   │ User's Browser     │
   │ Deletes Cookie     │
   │ (sessionid cleared)│
   └────────────────────┘
```

## Session Persistence Across Requests

```
Request 1: GET /
           │
           ├─ User sends: Cookie: sessionid=abc123
           │
           ├─ Middleware:
           │  └─ Load session from DB using sessionid
           │
           └─ Session available in view
              └─ request.session['user'] = "username"
                 └─ Rendered page with username

         ────────────────────────────────────────

Request 2: GET /dashboard
           │
           ├─ User sends: Cookie: sessionid=abc123
           │  (Same cookie!)
           │
           ├─ Middleware:
           │  └─ Load session from DB using same sessionid
           │  └─ Update: last_activity = now()
           │
           └─ Session still available
              └─ request.session['user'] = "username"
                 └─ Dashboard page loads with user info

         ────────────────────────────────────────

Request 3: GET /profile
           │
           ├─ User sends: Cookie: sessionid=abc123
           │  (Same cookie!)
           │
           ├─ Middleware:
           │  └─ Load session from DB using same sessionid
           │  └─ Update: last_activity = now()
           │
           └─ Session still available
              └─ request.session['user'] = "username"
                 └─ Profile page loads with user info

         ────────────────────────────────────────
         Session persists for 14 days until:
         - User logs out, OR
         - 14 days of inactivity, OR
         - Browser deletes cookie
```

## Middleware Processing Order

```
HTTP Request Arrives
         │
         ├─────────────────────────────────────────────┐
         │                                             │
    ┌────▼─────────────────────────────────────────┐  │
    │ 1. SecurityMiddleware                        │  │
    │    (HTTPS, Security headers)                 │  │
    └────┬──────────────────────────────────────────┘  │
         │                                             │
    ┌────▼─────────────────────────────────────────┐  │
    │ 2. SessionMiddleware (Django's built-in)    │  │
    │    (Initialize request.session object)      │  │
    └────┬──────────────────────────────────────────┘  │
         │                                             │
    ┌────▼─────────────────────────────────────────┐  │
    │ 3. CommonMiddleware                          │  │
    │    (URL normalization)                       │  │
    └────┬──────────────────────────────────────────┘  │
         │                                             │
    ┌────▼─────────────────────────────────────────┐  │
    │ 4. CsrfViewMiddleware                        │  │
    │    (CSRF protection)                         │  │
    └────┬──────────────────────────────────────────┘  │
         │                                             │
    ┌────▼─────────────────────────────────────────┐  │
    │ 5. AuthenticationMiddleware                  │  │
    │    (Populate request.user)                   │  │
    └────┬──────────────────────────────────────────┘  │
         │                                             │
    ┌────▼─────────────────────────────────────────┐  │
    │ 6. WhiteNoiseMiddleware                      │  │
    │    (Static files serving)                    │  │
    └────┬──────────────────────────────────────────┘  │
         │                                             │
    ┌────▼─────────────────────────────────────────┐  │
    │ 7. SessionManagementMiddleware (CUSTOM) ◄───┼──┘
    │    ✓ Create session if needed                │
    │    ✓ Load from DB                            │
    │    ✓ Update last_activity                    │
    │    ✓ Make data available                     │
    └────┬──────────────────────────────────────────┘
         │
    ┌────▼─────────────────────────────────────────┐
    │ 8. SessionExpiryMiddleware (CUSTOM)          │
    │    ✓ Check expiry                            │
    │    ✓ Cleanup logic                           │
    └────┬──────────────────────────────────────────┘
         │
         ├─ Now: request.session fully loaded
         │       and available in view
         │
    ┌────▼─────────────────────────────────────────┐
    │ VIEW PROCESSING                              │
    │ (Your application code)                      │
    └────┬──────────────────────────────────────────┘
         │
    ┌────▼─────────────────────────────────────────┐
    │ RESPONSE GENERATION                          │
    │ (Render template, return JSON, etc)          │
    └────┬──────────────────────────────────────────┘
         │
         └─ Response returned through middleware
            (in reverse order) ──► User's Browser
```

## Session Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                  DJANGO APPLICATION                         │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ request.session (Dictionary-like object)            │   │
│  │                                                      │   │
│  │ {'user': 'john',                                     │   │
│  │  'user_id': 1,                                       │   │
│  │  'user_email': 'john@example.com',                   │   │
│  │  'user_name': 'John Doe',                            │   │
│  │  'user_role': 2,                                     │   │
│  │  'user_status': 1,                                   │   │
│  │  'login_time': '2026-01-25T10:30:00',               │   │
│  │  'last_activity': '2026-01-25T10:35:00'}             │   │
│  └──────────┬───────────────────────────────────────────┘   │
│             │ Serialized to JSON                            │
│             │                                               │
│  ┌──────────▼───────────────────────────────────────────┐   │
│  │ Encrypted String (for database storage)             │   │
│  │                                                      │   │
│  │ Encrypted: abc123...xyz789                           │   │
│  └──────────┬───────────────────────────────────────────┘   │
│             │                                               │
│             └─────────────────┐                            │
│                               │                            │
└───────────────────────────────┼────────────────────────────┘
                                │
                    ┌───────────▼──────────────┐
                    │   MySQL Database         │
                    │   (drf_db)               │
                    │                          │
                    │  Table: django_session  │
                    │  ──────────────────────  │
                    │  session_key: 'abc123'  │
                    │  session_data: 'xyz...'  │
                    │  expire_date: 2026-02-08│
                    └────────────────────────┘
                                │
                    ┌───────────▼──────────────┐
                    │  User's Browser         │
                    │                         │
                    │  Cookie Storage:       │
                    │  ───────────────      │
                    │  sessionid=abc123     │
                    │  (14-day expiry)      │
                    │  (HTTPOnly flag)      │
                    │  (SameSite=Lax)       │
                    └────────────────────────┘
                                │
                    ┌───────────▼──────────────┐
                    │  Every HTTP Request    │
                    │                         │
                    │  GET / HTTP/1.1        │
                    │  Cookie: sessionid=... │
                    │  ...                   │
                    └────────────────────────┘
```

## Access Points

```
┌────────────────────────────────────────────────────────┐
│  Where Can You Access Session Data?                    │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. IN VIEWS                                          │
│     └─ request.session.get('user')                    │
│     └─ request.session['user_id']                     │
│     └─ get_session_user(request)                      │
│                                                        │
│  2. IN TEMPLATES                                      │
│     └─ {{ request.session.user }}                     │
│     └─ {{ request.session.user_email }}               │
│     └─ {% if request.session.user %}                  │
│                                                        │
│  3. IN DECORATORS                                     │
│     └─ @session_required                             │
│     └─ @session_required_ajax                        │
│                                                        │
│  4. IN MIDDLEWARE                                     │
│     └─ request.session (in process_request)          │
│     └─ request.session (in process_response)         │
│                                                        │
│  5. IN CLASS-BASED VIEWS                              │
│     └─ self.request.session.get('user')              │
│                                                        │
│  6. IN CONTEXT PROCESSORS                             │
│     └─ request.session (accessible)                   │
│                                                        │
│  7. IN SIGNALS/RECEIVERS                              │
│     └─ Need to pass via function parameters           │
│                                                        │
│  8. IN ASYNC TASKS/CELERY                             │
│     └─ Need to serialize and pass data                │
│                                                        │
└────────────────────────────────────────────────────────┘
```

---

**Updated**: January 25, 2026  
**Status**: ✅ Complete Implementation
