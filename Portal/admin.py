from django.contrib import admin
from .models import Exam, Question, StudentAttempt, StudentAnswer

admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(StudentAttempt)
admin.site.register(StudentAnswer)
