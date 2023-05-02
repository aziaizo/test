from django.urls import path
from .views import *
create_list = {'get': 'list', 'post': 'post'}


urlpatterns = [
    path('login/',LoginViewSet.as_view(create_list)),
    path('register/',RegisterViewSet.as_view(create_list)),
    path('confirm/', ConfirmationAPIView.as_view()),
    path('image/', ImageAPIView.as_view(), name='upload')
]