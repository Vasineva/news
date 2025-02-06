from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.models import Group, User
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm, ProfileUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView



class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'sign/profile_form.html'
    form_class = ProfileUpdateForm
    success_url = '/'

    def get_object(self):
        return self.request.user



class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'

@login_required
def user_profile(request):
    return render(request, 'index.html', {'user': request.user})

@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect('/')
