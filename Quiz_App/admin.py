from django.contrib import admin
from .models import Category, Question, Answer

# To make the admin interface more user-friendly, we can customize how models are displayed.

class AnswerInline(admin.TabularInline):
    """
    Allows for the inline editing of Answers directly within the Question admin page.
    This is more efficient than managing Questions and Answers separately.
    """
    model = Answer
    extra = 3 # Provides 3 empty slots for new answers by default.
    fields = ('answer_text', 'is_correct')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Custom admin view for the Question model.
    """
    # Displays these fields in the question list view.
    list_display = ('question_text', 'category', 'marks', 'created_at')
    # Adds a filter sidebar to filter questions by category.
    list_filter = ('category',)
    # Adds a search bar to search by question text.
    search_fields = ('question_text', 'category__name')
    # Integrates the inline Answer editor into the Question detail page.
    inlines = [AnswerInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Custom admin view for the Category model.
    """
    # Displays the category name in the list view.
    list_display = ('name',)
    # Adds a search bar to search by category name.
    search_fields = ('name',)

# Note: We don't need to register the Answer model separately
# because it is already managed through the QuestionAdmin via AnswerInline.
# If you wanted to manage Answers independently, you would use:
# admin.site.register(Answer)
