from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserUpdateForm, UserProfileForm
from .models import UserProfile

class AdminOnlyView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'is_staff'


class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created successfully! You can now log in.")
            return redirect('login')
        return render(request, 'accounts/register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        return render(request, 'accounts/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('profile')
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        profile, created = UserProfile.objects.get_or_create(
            user=request.user,
            defaults={'role': 'default_role'}
        )
        return render(request, 'accounts/profile.html', {'profile': profile})


class EditProfileView(LoginRequiredMixin, View):
    def get(self, request):
        profile, created = UserProfile.objects.get_or_create(
            user=request.user,
            defaults={'role': 'default_role'}
        )
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileForm(instance=profile)
        return render(request, 'accounts/edit_profile.html', {'u_form': u_form, 'p_form': p_form})

    def post(self, request):
        profile, created = UserProfile.objects.get_or_create(
            user=request.user,
            defaults={'role': 'default_role'}
        )
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UserProfileForm(request.POST, request.FILES, instance=profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('profile')

        return render(request, 'accounts/edit_profile.html', {'u_form': u_form, 'p_form': p_form})
