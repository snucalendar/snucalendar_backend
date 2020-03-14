from django.contrib import admin
from .models import Event, Posting, EventComment, QnA

# Register your models here.


admin.site.register(Event)
admin.site.register(Posting)
admin.site.register(EventComment)
admin.site.register(QnA)

