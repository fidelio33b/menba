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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


# To view the profile
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'zaccount/profile.html'


# To reset the password
class PasswordResetView(LoginRequiredMixin, TemplateView):
    template_name = 'zaccount/password_reset_form.html'


# To confirm the password reset
class PasswordResetConfirmView(LoginRequiredMixin, TemplateView):
    template_name = 'zaccount/password_reset_confirm.html'


# When the password reset is done
class PasswordResetDoneView(TemplateView):
    template_name = 'zaccount/password_reset_done.html'


class PasswordResetCompleteView(TemplateView):
    template_name = 'zaccount/password_reset_complete.html'
