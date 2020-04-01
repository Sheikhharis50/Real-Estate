from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from contacts.models import Contact


def login(request):
    if request.method == 'POST':
        # get form values
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')

        messages.error(request, 'User does not exists')
        return redirect('login')

    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, "You are now logged out")
        return redirect('index')


@login_required
def dashboard(request):
    
    if request.user.is_authenticated:
        user_id = request.user.id
        contacts = Contact.objects.all().filter(user_id=user_id)
        context = {
            'contacts': contacts
        }
        return render(request, 'accounts/dashboard.html', context)


def register(request):
    if request.method == 'POST':
        # get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # check if passwords are matched
        if password == password2:
            # Check Username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('register')
            else:
                # Check email
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'email already exists')
                    return redirect('register')
                else:
                    # Looks Good
                    user = User.objects.create_user(username=username,
                                                    password=password, email=email,
                                                    first_name=first_name, last_name=last_name)

                    # auth.login(request, user)
                    # messages.success(request, 'You are now logged in')
                    # return redirect('index')

                    user.save()
                    messages.success(request, 'You are now Registered')
                    return redirect('login')

        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

    else:
        return render(request, 'accounts/register.html')
