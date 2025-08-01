from django.urls import path
from . import views

# Define URL patterns for the Quiz_App
urlpatterns = [
    # The root path now points to the home view, which handles auth redirection
    path('', views.home, name='home'),
    
    # Auth URLs
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Quiz URLs
    path('quiz/<int:category_id>/', views.quiz, name='quiz'),
    path('results/<int:category_id>/', views.results, name='results'),
]
