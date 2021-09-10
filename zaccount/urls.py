"""
This file is part of Menba.
Copyright (C) 2021

Menba is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Menba is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Menba.  If not, see <https://www.gnu.org/licenses/>.

Laurent Lavaud <fidelio33b@gmail.com>, 2021.
"""

from django.contrib.auth import views as auth_views
from django.urls import path

from zaccount import views as zaccount

app_name = 'zaccount'

urlpatterns = [
    # Login and logout pages
    path('login/', auth_views.LoginView.as_view(template_name='zaccount/login.html'), name='alogin'),
    path('logout/', auth_views.LogoutView.as_view(template_name='zaccount/logout.html'), name='alogout'),

    # Redirected requests after login : profile page
    path('profile/', zaccount.ProfileView.as_view(), name='aprofile'),

    # Reset password
    path('password_reset/', zaccount.PasswordResetView.as_view(), name='apassword_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', zaccount.PasswordResetConfirmView.as_view(),
         name='apassword_reset_confirm'),
]
