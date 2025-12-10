# from django.shortcuts import render,redirect
# from django.contrib.auth import login, logout, authenticate
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
# from django.urls import reverse_lazy
# from .forms import UserRegistrationForm,UserLoginForm, UserProfileForm
# # Create your views here.
# def register_view(request):
#     if request.user.is_authenticated:
#         return redirect('media_assets:dashboard')
    
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             messages.success(request, f'Registration successful.')
#             return redirect('media_assets:dashboard')
#     else:
#         form = UserRegistrationForm()
#         return render(request, 'accounts/register.html', {'form': form})
    
# def login_view(request):
#     if request.user.is_authenticated:
#         return redirect('media_assets:dashboard')
#     if request.method == 'POST':
#         form = UserLoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate( username, password)
#             if user is not None:
#                 login(request, user)
#                 messages.success(request, f'Login successful.')
#                 return redirect('media_assets:dashboard')

#     else:
#         form = UserLoginForm()
#         return render(request, 'accounts/login.html', {'form': form})
        
# @login_required
# def logout_view(request):
#     logout(request)
#     messages.info(request,f"You have successfully logged out.")
#     return redirect('accounts:login')

# @login_required
# def profile_view(request):
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, request.FILES, instance=request.user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, f"Profile updated successfully.")
#             return redirect('accounts:profile')
#     else:
#         form = UserProfileForm(instance=request.user)
#     return render(request, 'accounts/profile.html', {'form': form})


# class CustomPasswordResetView(PasswordResetView):
#     template_name = 'accounts/password_reset.html'
#     email_template_name = 'accounts/password_reset_email.html'
#     success_url = reverse_lazy('accounts:password_reset_done')


# class CustomPasswordResetConfirmView(PasswordResetConfirmView):
#     template_name = 'accounts/password_reset_confirm.html'
#     success_url = reverse_lazy('accounts:password_reset_complete')
                


from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm

# REGISTER VIEW
def register_view(request):
    if request.user.is_authenticated:
        return redirect('media_assets:dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('media_assets:dashboard')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


# LOGIN VIEW
def login_view(request):
    if request.user.is_authenticated:
        return redirect('media_assets:dashboard')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('media_assets:dashboard')
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('accounts:login')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})


class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')
