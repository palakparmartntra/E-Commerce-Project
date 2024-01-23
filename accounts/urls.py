
from django.urls import path,include
from . import views
urlpatterns = [
    path('update/<int:pk>/',views.UpdateAddressView.as_view(),name='update'),
    path('y/<int:pk>/',views.UpdateUserProfile.as_view(),name='updateprofile'),

    path('index',views.index,name='index')

]
