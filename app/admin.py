from django.contrib import admin
from .models import CommentModel, ContentModel, CustomUser


admin.site.register(ContentModel)
admin.site.register(CustomUser)
admin.site.register(CommentModel)

