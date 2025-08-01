from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Question, Answer
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
import random

def home(request):
    """
    If the user is authenticated, show the quiz categories.
    Otherwise, redirect them to the login page.
    """
    if request.user.is_authenticated:
        categories = Category.objects.all()
        return render(request, 'home.html', {'categories': categories})
    return redirect('login')


# --- User Authentication Views ---

def register_view(request):
    """
    Handles user registration. Redirects home if already logged in.
    """
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    """
    Handles user login. Redirects home if already logged in.
    """
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    """
    Logs the user out and redirects to the login page.
    """
    logout(request)
    return redirect('login')


# --- Quiz Views (Protected) ---

@login_required
def quiz(request, category_id):
    """
    Handles the main quiz logic. Requires user to be logged in.
    """
    category = get_object_or_404(Category, id=category_id)

    if 'quiz_questions' not in request.session or request.session.get('current_category_id') != category_id:
        questions = list(category.questions.all())
        random.shuffle(questions)
        request.session['quiz_questions'] = [q.id for q in questions]
        request.session['score'] = 0
        request.session['question_number'] = 0
        request.session['current_category_id'] = category_id

    question_ids = request.session['quiz_questions']
    question_number = request.session['question_number']

    if question_number >= len(question_ids):
        return redirect('results', category_id=category_id)

    current_question_id = question_ids[question_number]
    question = get_object_or_404(Question, id=current_question_id)

    if request.method == 'POST':
        selected_answer_id = request.POST.get('answer')
        if selected_answer_id:
            selected_answer = get_object_or_404(Answer, id=selected_answer_id)
            if selected_answer.is_correct:
                request.session['score'] += question.marks

        request.session['question_number'] += 1
        return redirect('quiz', category_id=category_id)

    context = {
        'question': question,
        'category': category,
        'total_questions': len(question_ids)
    }
    return render(request, 'quiz.html', context)

@login_required
def results(request, category_id):
    """
    Displays the final quiz results. Requires user to be logged in.
    """
    category = get_object_or_404(Category, id=category_id)
    score = request.session.get('score', 0)
    total_questions = len(request.session.get('quiz_questions', []))
    
    if total_questions > 0:
        percentage_raw = (score / total_questions) * 100
        percentage = round(percentage_raw)
        circumference = 2 * 3.14159 * 45
        stroke_dasharray = (percentage_raw / 100) * circumference
    else:
        percentage = 0
        stroke_dasharray = 0

    context = {
        'category': category,
        'score': score,
        'total_questions': total_questions,
        'percentage': percentage,
        'percentage_for_svg': stroke_dasharray,
    }
    
    for key in ['quiz_questions', 'score', 'question_number', 'current_category_id']:
        if key in request.session:
            del request.session[key]

    return render(request, 'results.html', context)
