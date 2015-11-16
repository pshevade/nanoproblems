from django.contrib import admin

# Register your models here.

from .models import Comment, Question, Answer

admin.site.register(Comment)
admin.site.register(Question)
admin.site.register(Answer)
