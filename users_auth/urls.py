from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    LoginUser, UpdateUser, UserProfile
)
urlpatterns = [
    path('login/', LoginUser.as_view(), name='log_in'),
    path('logout/', LogoutView.as_view(next_page='home'), name='log_out' ),
    path('account/edit/<int:pk>/', UpdateUser.as_view(), name="update_user"),
    path('account/<int:pk>/', UserProfile.as_view(), name="view_profile"),
]
