from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import User, Message
from .forms import ComposeForm
from django.http import JsonResponse


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('inbox')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def inbox_view(request):
    if request.user.is_authenticated:
        messages = Message.objects.all()
        user = User.objects.all()
        # messages = Message.objects.filter(recipient=request.user)

        return render(request, 'inbox.html', {'messages': messages,'user': user,})
    else:
        return redirect('login')


def chat_view(request):
    if request.user.is_authenticated:
        messages = Message.objects.all()
        # messages = Message.objects.filter(recipient=request.user)

        return JsonResponse({'messages': messages})
    else:
        return redirect('login')




def delete_message(request, id):
    if request.user.is_authenticated:
        message = Message.objects.get(id=id)
        message.delete()
        return redirect('inbox')
    else:
        return redirect('login')


def compose_message(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ComposeForm(request.POST)
            if form.is_valid():
                sender = request.user
                recipient_username = form.cleaned_data['recipient']
                recipient = get_object_or_404(User, username=recipient_username)
                # subject = form.cleaned_data['subject']
                body = form.cleaned_data['body']
                Message.objects.create(sender=sender, recipient=recipient, body=body)
                return redirect('inbox')
        else:
            form = ComposeForm()
        return render(request, 'inbox.html', {'form': form})
    else:
        return redirect('login')


def edit_message(request, id):
    if request.user.is_authenticated:
        message = Message.objects.get(id=id)
        if request.method == 'POST':
            form = ComposeForm(request.POST)
            if form.is_valid():
                message.recipient = get_object_or_404(User, username=form.cleaned_data['recipient'])
                # message.subject = form.cleaned_data['subject']
                message.body = form.cleaned_data['body']
                message.save()
                return redirect('inbox')
        else:
            form = ComposeForm(initial={'recipient': message.recipient.username, 'body': message.body})
        return render(request, 'edit.html', {'form': form})
    else:
        return redirect('login')
