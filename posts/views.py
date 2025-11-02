from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from posts.forms import RegistrationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

User = get_user_model()
def index(request):
    return render(request, 'index.html')

class PostsLoginView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('posts:profile')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('posts:index')
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('posts:index')

@login_required
def profile(request):
    context = {'user': request.user}
    return render(request, 'profile.html', context)