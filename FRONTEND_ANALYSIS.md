# Flight-Ticket-Booking Frontend Analysis Report

## Repository URL
https://github.com/Rakshitak21/Flight-Ticket-Booking

---

## 1. Frontend Technology Stack

**Framework Type:** Django Templates with Vanilla HTML/CSS/JavaScript (NOT React, Vue, or modern SPA framework)

### Technology Details:
- **Frontend:** HTML5, CSS3, Vanilla JavaScript (ES5)
- **Backend:** Python Django 5.0.1
- **CSS Framework:** Bootstrap 4.4.1
- **jQuery:** jQuery 3.4.1
- **Database:** SQLite
- **Server:** Gunicorn
- **Additional Libraries:** BeautifulSoup4, Pandas, Prometheus Client

---

## 2. Complete Frontend Directory Structure

```
frontend-repo/
├── flight/                           # Main Django App
│   ├── templates/                    # HTML Templates (Django Templates)
│   │   └── flight/
│   │       ├── book.html             # Flight booking page
│   │       ├── bookings.html         # User bookings history
│   │       ├── index.html            # Home page
│   │       ├── layout.html           # Base template (navigation & footer)
│   │       ├── layout2.html          # Alternative layout
│   │       ├── login.html            # User login page
│   │       ├── payment.html          # Payment page
│   │       ├── payment_process.html  # Payment processing page
│   │       ├── register.html         # User registration page
│   │       └── search.html           # Flight search results
│   │
│   ├── static/                       # Static Assets
│   │   ├── css/                      # Stylesheets
│   │   │   ├── bookings_style.css
│   │   │   ├── book_style.css
│   │   │   ├── layout_style.css
│   │   │   ├── payment_process_style.css
│   │   │   ├── payment_style.css
│   │   │   ├── search2_style.css
│   │   │   ├── search_style.css
│   │   │   └── styles2.css
│   │   │
│   │   ├── js/                       # JavaScript Files
│   │   │   ├── book.js               # Booking page logic
│   │   │   ├── bookings.js           # User bookings logic
│   │   │   ├── index.js              # Home page logic
│   │   │   ├── layout.js             # Navigation & layout logic
│   │   │   ├── payment_process.js    # Payment processing logic
│   │   │   ├── search.js             # Flight search logic
│   │   │   ├── search2.js            # Alternative search logic
│   │   │   ├── signin.js             # Sign-in logic
│   │   │   └── signup.js             # Sign-up logic
│   │   │
│   │   └── img/                      # Images & Icons
│   │       ├── about-us.png
│   │       ├── about-us-cms.png
│   │       ├── card.png
│   │       ├── contactbg.svg
│   │       ├── destination.png
│   │       ├── earth.jfif
│   │       ├── evening_active.png
│   │       ├── evening_inactive.png
│   │       ├── favicon.ico
│   │       ├── flight-bg1.jpg
│   │       ├── flight-bg2.jpg
│   │       ├── flight_icon.png
│   │       ├── icon.png
│   │       ├── icon_logo.png
│   │       ├── icon_logo_white-outline.png
│   │       ├── morning_active.png
│   │       ├── morning_inactive.png
│   │       ├── newsletter.png
│   │       ├── night_active.png
│   │       ├── night_inactive.png
│   │       ├── noon_active.png
│   │       ├── noon_inactive.png
│   │       ├── plane3.1.jfif
│   │       ├── plane3.1.jpg
│   │       ├── plane3.12.jpg
│   │       ├── plane3.jfif
│   │       ├── plane4.jfif
│   │       ├── privacy-policy.png
│   │       ├── process.gif
│   │       ├── sky.jfif
│   │       └── terms-and-conditions.png
│   │
│   ├── migrations/                   # Database migrations
│   ├── admin.py                      # Django admin configuration
│   ├── apps.py                       # App configuration
│   ├── models.py                     # Database models
│   ├── views.py                      # View controllers (Django MVT)
│   ├── urls.py                       # URL routing
│   ├── utils.py                      # Utility functions
│   ├── tests.py                      # Unit tests
│   ├── constant.py                   # Constants (fees, surcharges)
│   ├── metrics.py                    # Prometheus metrics
│   ├── middleware.py                 # Custom middleware
│   └── __init__.py
│
├── capstone/                         # Main Django Project
│   └── (project settings & utilities)
│
├── Data/                             # Data files
│   ├── add_places.py
│   ├── airports.csv
│   ├── domestic_flights.csv
│   └── international_flights.csv
│
├── k8s/                              # Kubernetes configs
│
├── manage.py                         # Django management script
├── requirements.txt                  # Python dependencies
├── Dockerfile                        # Docker configuration
├── docker-compose.yml                # Docker Compose setup
├── .env.example                      # Environment variables template
├── .gitignore                        # Git ignore rules
└── README.md                         # Project documentation
```

---

## 3. Frontend Files Listing by Category

### HTML Templates (10 files)
| File | Purpose |
|------|---------|
| `templates/flight/layout.html` | Base layout with navigation & footer |
| `templates/flight/layout2.html` | Alternative base layout |
| `templates/flight/index.html` | Home/Landing page with flight search form |
| `templates/flight/search.html` | Flight search results page |
| `templates/flight/book.html` | Booking confirmation page |
| `templates/flight/bookings.html` | User's booking history |
| `templates/flight/login.html` | User login page |
| `templates/flight/register.html` | User registration page |
| `templates/flight/payment.html` | Payment information page |
| `templates/flight/payment_process.html` | Payment processing page |

### CSS Stylesheets (8 files)
| File | Purpose |
|------|---------|
| `static/css/layout_style.css` | Navigation, footer, & base styles |
| `static/css/styles2.css` | General page styles |
| `static/css/search_style.css` | Flight search form & results styling |
| `static/css/search2_style.css` | Alternative search styling |
| `static/css/book_style.css` | Booking page styling |
| `static/css/bookings_style.css` | User bookings history styling |
| `static/css/payment_style.css` | Payment page styling |
| `static/css/payment_process_style.css` | Payment processing styling |

### JavaScript Files (9 files)
| File | Purpose |
|------|---------|
| `static/js/layout.js` | Navigation, dropdown menus, responsive behavior |
| `static/js/index.js` | Home page flight search logic & validation |
| `static/js/search.js` | Flight search results page functionality |
| `static/js/search2.js` | Alternative search page functionality |
| `static/js/book.js` | Booking page logic & seat selection |
| `static/js/bookings.js` | User bookings page interactions |
| `static/js/payment_process.js` | Payment processing logic |
| `static/js/signin.js` | Login form validation & submission |
| `static/js/signup.js` | Registration form validation & submission |

### Images & Assets (38 files)
- Background images: `flight-bg1.jpg`, `flight-bg2.jpg`, `sky.jfif`
- UI Images: `about-us.png`, `destination.png`, `process.gif`, `card.png`
- Time-based icons: `morning_active.png`, `noon_active.png`, `evening_active.png`, `night_active.png` (+ inactive variants)
- Logos: `icon_logo.png`, `icon_logo_white-outline.png`, `icon.png`, `flight_icon.png`
- Policy images: `privacy-policy.png`, `terms-and-conditions.png`
- Favicon: `favicon.ico`

---

## 4. Key Configuration Files for Frontend

### Python Dependencies (requirements.txt)
```
Django==5.0.1
asgiref==3.7.2
sqlparse==0.4.4
gunicorn==21.2.0
python-decouple==3.8
whitenoise==6.6.0
beautifulsoup4
pandas
prometheus_client>=0.16.0
```

### External Dependencies (CDN/Libraries)
- **Bootstrap 4.4.1** - CSS framework via CDN
- **jQuery 3.4.1** - DOM manipulation
- **Typekit fonts** - Custom typography
- **Popper.js** - Tooltip/dropdown positioning

### Docker Configuration
- **Dockerfile** - Container image setup
- **docker-compose.yml** - Multi-container orchestration
- **Kubernetes configs** - K8s deployment files in `k8s/` directory

---

## 5. Frontend Architecture

### Architecture Type
**Server-Side Rendered (SSR) with Django Templates**
- Not a Single Page Application (SPA)
- Not a modern JavaScript framework (React/Vue)
- Traditional MVC/MVT architecture (Django Model-View-Template)

### Request Flow
1. User requests page → Django view processes request
2. View renders Django template with context data
3. Template generates HTML + embedded CSS/JS
4. Browser receives complete HTML + assets
5. Vanilla JavaScript handles client-side interactions

### Features
- **Authentication:** Django built-in auth system
- **Template Inheritance:** Base layout extended by child templates
- **Form Handling:** Django forms with CSRF protection
- **Dynamic Content:** Server-side rendering with context variables
- **Client-side Validation:** Vanilla JavaScript validation
- **Responsive Design:** Bootstrap Grid system

---

## 6. Key Files to Copy for Frontend Migration

### Essential Files
```
✓ flight/templates/flight/*.html          (All 10 HTML files)
✓ flight/static/css/*.css                 (All 8 CSS files)
✓ flight/static/js/*.js                   (All 9 JavaScript files)
✓ flight/static/img/*                     (All 38 image assets)
✓ flight/views.py                         (View logic)
✓ flight/urls.py                          (URL routing)
✓ flight/models.py                        (Database models)
✓ flight/serializers.py                   (Data serialization if needed)
```

### Configuration Files
```
✓ requirements.txt                        (Python dependencies)
✓ manage.py                               (Django management)
✓ capstone/settings.py                    (Django settings)
✓ capstone/urls.py                        (Project URLs)
✓ Dockerfile                              (Container setup)
✓ docker-compose.yml                      (Container orchestration)
✓ .env.example                            (Environment template)
```

### Data & Utilities
```
✓ flight/constant.py                      (Fee/surcharge constants)
✓ flight/utils.py                         (Helper functions)
✓ Data/*.csv                              (Flight data)
✓ Data/add_places.py                      (Data loading script)
```

---

## 7. Build & Deployment Configuration

### Build Process
- **No build tool needed** (not Webpack/Vite/etc.)
- **Static files collection:** `python manage.py collectstatic`
- **Database migrations:** `python manage.py migrate`
- **Server:** Gunicorn WSGI server

### Deployment Options
1. **Docker:** Pre-configured Dockerfile & docker-compose.yml
2. **Kubernetes:** K8s deployment manifests in `k8s/` folder
3. **Traditional Server:** Direct Django runserver or Gunicorn

### Environment Variables
See `.env.example` for required configuration

---

## 8. Frontend Framework Summary

| Aspect | Details |
|--------|---------|
| **Type** | Server-Side Rendered (SSR) Django Application |
| **UI Framework** | Bootstrap 4.4.1 (CSS only) |
| **JavaScript** | Vanilla ES5 (no transpilation) |
| **Package Manager** | pip (Python) - not npm |
| **Build Tool** | None (Django collectstatic) |
| **Templates** | Django Template Language (.html files) |
| **Styling** | CSS3 with Bootstrap classes |
| **Component System** | Django template inheritance |
| **Routing** | Django URL patterns (server-side) |
| **State Management** | Django session + server-side rendering |

---

## 9. Frontend Pages Overview

### Public Pages
- **Home (index.html)** - Landing page with flight search form
- **Search (search.html)** - Flight search results display
- **Login (login.html)** - User authentication
- **Register (register.html)** - User registration

### Authenticated Pages
- **Book (book.html)** - Booking confirmation & details
- **Bookings (bookings.html)** - User's booking history
- **Payment (payment.html)** - Payment information entry
- **Payment Process (payment_process.html)** - Payment processing

### Base Component
- **Layout (layout.html)** - Navigation bar, footer, base structure

---

## 10. Total Asset Count

| Category | Count |
|----------|-------|
| HTML Templates | 10 |
| CSS Stylesheets | 8 |
| JavaScript Files | 9 |
| Images/Icons | 38 |
| **Total Frontend Files** | **65+** |

---

## Notes for Integration

1. **Not a Standalone Frontend** - This is a Django monolith, not a separate frontend service
2. **No Node.js Dependency** - Requires Python & Django, not Node.js
3. **Server-Side Rendering** - All HTML is rendered on the server, sent to browser
4. **Static Files** - All CSS/JS/images are served from Django's static file handler
5. **No API Separation** - Frontend and backend are tightly coupled in Django app
6. **Database Integrated** - Frontend directly depends on Django models and database

---

## Deployment in Your Microservices Architecture

To integrate this into your microservices (currently using auth-service, booking-service, flight-service):

1. **Option A: Separate Frontend Service**
   - Extract frontend files into a new service
   - Create a Node.js/Express or React SPA
   - Call your microservices via APIs

2. **Option B: Keep Django Monolith**
   - Keep this as-is with microservices as backend APIs
   - Update frontend to call auth-service, booking-service, flight-service endpoints

3. **Option C: Hybrid Approach**
   - Use existing frontend with microservices
   - Update views.py to call your microservices instead of local models
