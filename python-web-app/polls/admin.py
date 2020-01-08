from django.contrib import admin

from .models import Question

admin.site.register(Question) # makes the Question type
  # visible, modifiable from the /admin page
