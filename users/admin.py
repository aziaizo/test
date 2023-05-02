from django.contrib import admin
from users.models import UserModel, Image

class ImageAdmin(admin.ModelAdmin):
    list_display = ["image"]


admin.site.register(UserModel)

admin.site.register(Image)
