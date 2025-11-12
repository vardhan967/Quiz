from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse
from django.forms import modelform_factory
from .models import Category, Question, Answer
from .forms import CategoryForm, QuestionForm, AnswerFormSet
from django.http import HttpResponseForbidden


def host_required(view_func):
    """Decorator that allows only staff users or users in 'Host' group."""
    def _wrapped(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return redirect('login')
        if not (user.is_staff or user.groups.filter(name='Host').exists()):
            return HttpResponseForbidden('You do not have permission to access this page.')
        return view_func(request, *args, **kwargs)
    return _wrapped


@host_required
def dashboard(request):
    categories_count = Category.objects.count()
    questions_count = Question.objects.count()
    answers_count = Answer.objects.count()
    return render(request, 'host_panel/dashboard.html', {
        'categories_count': categories_count,
        'questions_count': questions_count,
        'answers_count': answers_count,
    })


# Category CRUD
@host_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'host_panel/category_list.html', {'categories': categories})


@host_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('host_category_list')
    else:
        form = CategoryForm()
    return render(request, 'host_panel/category_form.html', {'form': form, 'title': 'Create Category'})


@host_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('host_category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'host_panel/category_form.html', {'form': form, 'title': 'Edit Category'})


@host_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('host_category_list')
    return render(request, 'host_panel/confirm_delete.html', {'object': category, 'type': 'Category'})


# Question CRUD with Answer inline formset
@host_required
def question_list(request):
    questions = Question.objects.select_related('category').all()
    return render(request, 'host_panel/question_list.html', {'questions': questions})


@host_required
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save()
            formset = AnswerFormSet(request.POST, instance=question)
            if formset.is_valid():
                formset.save()
                return redirect('host_question_list')
        else:
            formset = AnswerFormSet(request.POST)
    else:
        form = QuestionForm()
        formset = AnswerFormSet()

    return render(request, 'host_panel/question_form.html', {'form': form, 'formset': formset, 'title': 'Create Question'})


@host_required
def question_edit(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = AnswerFormSet(request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('host_question_list')
    else:
        form = QuestionForm(instance=question)
        formset = AnswerFormSet(instance=question)
    return render(request, 'host_panel/question_form.html', {'form': form, 'formset': formset, 'title': 'Edit Question'})


@host_required
def question_delete(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        question.delete()
        return redirect('host_question_list')
    return render(request, 'host_panel/confirm_delete.html', {'object': question, 'type': 'Question'})

