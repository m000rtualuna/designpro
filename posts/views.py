from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import generic
from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from posts.forms import RegistrationForm, RequestForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils import timezone
from django.views import generic
from django.views.generic import CreateView, UpdateView, DeleteView
from posts.models import UserRequest

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
    user_requests = UserRequest.objects.filter(user=request.user)
    context = {'user': request.user, 'userrequest_list': user_requests}
    return render(request, 'profile.html', context)

@login_required
def create_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST, request.FILES)
        if form.is_valid():
            UserRequest = form.save(commit=False)
            UserRequest.user = request.user
            UserRequest.pub_date = timezone.now()
            UserRequest.save()
            return redirect('posts:index')
    else:
        form = RequestForm()
    return render(request, 'create_request.html', {'form': form,})

class UsersRequestListView(generic.ListView):
    model = UserRequest
    paginate_by = 4
    template_name = 'index.html'

    def get_queryset(self):
        return UserRequest.objects.filter(status='d')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accepted_count'] = UserRequest.objects.filter(status='a').count()
        return context

class RequestDetail(generic.DetailView):
    model = UserRequest
    template_name = 'request_detail.html'

class DeleteRequest(PermissionRequiredMixin, DeleteView):
    model = UserRequest
    success_url = reverse_lazy('posts:index')
    permission_required = 'posts.delete_userrequest'
    template_name = "delete_request.html"