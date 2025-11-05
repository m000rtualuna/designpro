from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from posts.forms import RegistrationForm, RequestForm, StatusChangeForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils import timezone
from django.views import generic
from django.views.generic import CreateView, UpdateView, DeleteView
from posts.models import UserRequest, Category
from .forms import CategoryForm
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator

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
    if request.user.is_staff:
        return render(request, 'admin_profile.html')

    status = request.GET.get('status')
    ALLOWED = {'n', 'a', 'd'}
    qs = UserRequest.objects.filter(user=request.user)
    if status in ALLOWED:
        qs = qs.filter(status=status)
    user_requests = qs.order_by('-pub_date')
    return render(request, 'profile.html', {
        'userrequest_list': user_requests,
        'current_status': status,
    })


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
    return render(request, 'create_request.html', {'form': form, })


class UsersRequestListView(generic.ListView):
    model = UserRequest
    paginate_by = 4
    template_name = 'index.html'

    def get_queryset(self):
        return UserRequest.objects.filter(status='d').order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accepted_count'] = UserRequest.objects.filter(status='a').count()
        return context


class RequestDetail(generic.DetailView):
    model = UserRequest
    template_name = 'request_detail.html'


class DeleteRequest(LoginRequiredMixin, DeleteView):
    model = UserRequest
    success_url = reverse_lazy('posts:index')
    template_name = "delete_request.html"

    def has_permission(self, request):
        obj = self.get_object()
        return obj.AdvUser == request.user


@staff_member_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('posts:category_list')
    else:
        form = CategoryForm()
    return render(request, 'category_list.html', {'form': form})


@staff_member_required
def category_list(request):
    categories = Category.objects.all().order_by('title')
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('posts:category_list')
    else:
        form = CategoryForm()
    return render(request, 'category_list.html', {'categories': categories, 'form': form})


@staff_member_required
def delete_category(request, pk):
    if request.method == 'POST':
        category = Category.objects.get(pk=pk)
        category.delete()
        return redirect('posts:category_list')
    return redirect('posts:category_list')


class AllRequests(generic.ListView):
    model = UserRequest
    template_name = 'all_requests.html'

    def get_queryset(self):
        return UserRequest.objects.all().order_by('-pub_date')


class ChangeRequestStatus(UpdateView):
    model = UserRequest
    form_class = StatusChangeForm
    template_name = 'admin_requests_detail.html'
    success_url = reverse_lazy('posts:all_requests')