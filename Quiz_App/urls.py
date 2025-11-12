from django.urls import path
from . import views
from . import host_views

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
    # Host admin panel
    path('host/', host_views.dashboard, name='host_dashboard'),
    path('host/categories/', host_views.category_list, name='host_category_list'),
    path('host/categories/create/', host_views.category_create, name='host_category_create'),
    path('host/categories/<int:pk>/edit/', host_views.category_edit, name='host_category_edit'),
    path('host/categories/<int:pk>/delete/', host_views.category_delete, name='host_category_delete'),

    path('host/questions/', host_views.question_list, name='host_question_list'),
    path('host/questions/create/', host_views.question_create, name='host_question_create'),
    path('host/questions/<int:pk>/edit/', host_views.question_edit, name='host_question_edit'),
    path('host/questions/<int:pk>/delete/', host_views.question_delete, name='host_question_delete'),
    # (Proctoring routes removed)
]
