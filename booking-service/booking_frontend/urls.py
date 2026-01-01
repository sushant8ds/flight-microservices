
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('static-test/', views.static_test_view, name='static_test'),
    path('static-diagnostic/', views.static_diagnostic_view, name='static_diagnostic'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register_view, name='register'),
    path('query/places/<str:q>', views.query_places, name='query_places'),
    path('flight', views.flight, name='flight'),
    path('review', views.review, name='review'),
    path('flight/ticket/book', views.book, name='book'),
    path('flight/ticket/payment', views.payment, name='payment'),
    path('flight/ticket/api/<str:ref>', views.ticket_data, name='ticketdata'),
    path('flight/ticket/print', views.get_ticket, name='getticket'),
    path('flight/bookings', views.bookings, name='bookings'),
    path('flight/ticket/cancel', views.cancel_ticket, name='cancelticket'),
    path('flight/ticket/resume', views.resume_booking, name='resumebooking'),
    path('contact', views.contact, name='contact'),
    path('privacy-policy', views.privacy_policy, name='privacypolicy'),
    path('terms-and-conditions', views.terms_and_conditions, name='termsandconditions'),
    path('about-us', views.about_us, name='aboutus'),
    # legacy routes for compatibility
    path('bookings/', views.bookings_list, name='bookings_list'),
    path('search-flights/', views.search_flights, name='search_flights'),
    path('book-flight/', views.book_flight, name='book_flight'),
]
