from django.contrib import admin

from .models import Question, Choice

admin.site.register(Question) # Makes the Question type visible,
                              # modifiable from the /admin page.

