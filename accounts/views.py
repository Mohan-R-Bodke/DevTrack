from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User

from django.contrib import messages

from .forms import RegisterForm, LoginForm


def register_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password != confirm_password:

                form.add_error(
                    'confirm_password',
                    'Passwords do not match.'
                )

            elif User.objects.filter(username=username).exists():

                form.add_error(
                    'username',
                    'Username already exists.'
                )

            elif User.objects.filter(email=email).exists():

                form.add_error(
                    'email',
                    'Email already exists.'
                )

            else:

                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )

                login(request, user)

                return redirect('dashboard')

    else:

        form = RegisterForm()

    return render(
        request,
        'register.html',
        {'form': form}
    )


def login_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':

        form = LoginForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:

                login(request, user)

                return redirect('dashboard')

            form.add_error(
                None,
                'Invalid username or password.'
            )

    else:

        form = LoginForm()

    return render(
        request,
        'login.html',
        {'form': form}
    )


def logout_view(request):

    logout(request)

    return redirect('login')