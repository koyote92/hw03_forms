from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from django.urls import reverse_lazy

from . import views


app_name = 'users'

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path(
        'login/',
        LoginView.as_view(template_name='users/login.html'),
        name='login'
    ),
    path(
      'logout/',
      LogoutView.as_view(template_name='users/logged_out.html'),
      name='logout'
    ),
    path('password_change/', auth_views.PasswordChangeView.as_view
         (template_name='users/password_change_form.html',
          success_url=reverse_lazy('users:password_change_done')),
         name='password_change_form'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view
         (template_name='users/password_change_done.html'),
         name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view
         (template_name='users/password_reset_form.html',
          email_template_name='users/password_reset_email.html',
          success_url=reverse_lazy('users:password_reset_done')),
         name='password_reset_form'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view
         (template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view
         (template_name='users/password_reset_confirm.html',
          success_url=reverse_lazy('users:password_reset_complete')),
         name='password_reset_confirm'),
    path('password_reset/complete/',
         auth_views.PasswordResetCompleteView.as_view
         (template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]
