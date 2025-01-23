from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect


def account_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('polygon_list')
    else:
        form = AuthenticationForm()

    return render(request, 'login_form.html', {'form': form})


def account_logout(request):
    logout(request)
    return redirect('account_login')
