
from django.shortcuts import redirect, render
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required





@login_required
def user_profile(request):
    return render(request, 'index.html', {'user': request.user})

@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='premium')
    if not request.user.groups.filter(name='premium').exists():
        premium_group.user_set.add(user)
    return redirect('/')
