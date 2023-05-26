from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View, ListView, CreateView, DeleteView
from booklet.models import Booklet

class LoginPageView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('booklet_list')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials.'})


class SignupPageView(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password != confirm_password:
            return render(request, 'signup.html', {'error': 'Passwords do not match.'})
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists.'})
        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email already exists.'})
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect('login')


class BookletListView(LoginRequiredMixin, ListView):
    model = Booklet
    template_name = 'booklet_list.html'
    context_object_name = 'booklets'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Booklet.objects.all()
        else:
            return Booklet.objects.filter(uploaded_by=self.request.user)


class BookletUploadView(LoginRequiredMixin, CreateView):
    model = Booklet
    fields = ['title', 'file']
    template_name = 'booklet_upload.html'
    success_url = reverse_lazy('booklet_list')

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)


class BookletDeleteView(LoginRequiredMixin, DeleteView):
    model = Booklet
    template_name = 'booklet_confirm_delete.html'
    success_url = reverse_lazy('booklet_list')
