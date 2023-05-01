from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # users
    path('api/v1/users/', include('users.urls'))
]
