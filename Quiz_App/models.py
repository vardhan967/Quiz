from django.db import models

class Category(models.Model):
    """
    Represents a category or topic for a set of questions.
    For example: "Science", "History", "General Knowledge".
    """
    name = models.CharField(max_length=100, unique=True, help_text="The name of the quiz category.")

    class Meta:
        # Orders categories alphabetically by name in the admin panel.
        ordering = ['name']
        # Sets the plural name for the model in the admin interface.
        verbose_name_plural = "Categories"

    def __str__(self):
        """String representation of the Category model."""
        return self.name

class Question(models.Model):
    """
    Represents a single question within a specific category.
    """
    category = models.ForeignKey(
        Category,
        related_name='questions', # Allows accessing questions from a category object, e.g., category.questions.all()
        on_delete=models.CASCADE,
        help_text="The category this question belongs to."
    )
    question_text = models.CharField(max_length=255, help_text="The text of the question.")
    marks = models.IntegerField(default=1, help_text="The points awarded for a correct answer.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="The date and time this question was created.")

    class Meta:
        # Orders questions by the date they were created.
        ordering = ['-created_at']

    def __str__(self):
        """String representation of the Question model."""
        return self.question_text

class Answer(models.Model):
    """
    Represents a possible answer/choice for a Question.
    Each question can have multiple answers, but only one is correct.
    """
    question = models.ForeignKey(
        Question,
        related_name='answers', # Allows accessing answers from a question object, e.g., question.answers.all()
        on_delete=models.CASCADE,
        help_text="The question this answer is associated with."
    )
    answer_text = models.CharField(max_length=255, help_text="The text of the answer choice.")
    is_correct = models.BooleanField(default=False, help_text="Mark this if the answer is correct.")

    def __str__(self):
        """String representation of the Answer model."""
        return f"{self.answer_text} (for: {self.question.question_text[:20]}...)"

