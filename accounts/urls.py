from django.urls import path
from .views import ViewProfile


urlpatterns = [
    path('<pk>/', ViewProfile.as_view(), name='view_profile'),
]
