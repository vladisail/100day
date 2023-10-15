from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout, update_session_auth_hash
from .forms import CustomPasswordChangeForm, AddFriendForm, SearchFriendsForm
from blog.forms import CommentForm
from blog.models import Post
from .models import Profile, Friend
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib import messages


def user_login(request):
    error_message = None
    if request.method == 'POST':
        # При вызове представления user_login с запросом методом GET посредством инструкции form = LoginForm()
        # создается экземпляр новой формы входа.
        # Затем эта форма передается в шаблон.
        # Если POST, то выполняем дальше действия
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/blog')
                else:
                    error_message = 'Аккаунт заблокирован'
            else:
                error_message = 'Неверный логин или пароль'
        else:
            error_message = 'Форма заполнена некорректно'
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form, 'error_message': error_message})


def user_logout(request):
    logout(request)
    return redirect('accounts:user_login')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создайте нового пользователя, но пока не сохраняйте его
            new_user = user_form.save(commit=False)
            # Установите пароль
            new_user.set_password(user_form.cleaned_data['password'])
            # Сохраните объект пользователя
            new_user.save()
            # Создайте профиль пользователя
            Profile.objects.create(user=new_user)
            login(request, new_user)
            return redirect('/blog')  # Перенаправьте пользователя после успешной регистрации
    else:
        user_form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            update_session_auth_hash(request, request.user)
            return redirect('accounts:profile', username=request.user.username)
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request,
                  'accounts/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    user_profile = Profile.objects.get(user=user)
    user_posts = Post.objects.filter(author=user, status='PB')
    form = CommentForm()
    return render(request, 'accounts/profile.html',
                  {'user_profile': user_profile,
                   'user_posts': user_posts,
                   'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Обновление сессии пользователя после смены пароля
            messages.success(request, 'Your password was successfully updated!')
            return redirect('accounts:profile', username=request.user.username)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'accounts/change_password.html', {'form': form})


@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    current_user = request.user
    user_posts = Post.objects.filter(author=user, status='PB')
    form = CommentForm()
    if current_user == user:
        user_profile = Profile.objects.get_or_create(user=user)[0]
        return render(request, 'accounts/profile.html',
                  {'user': user,
                   'user_profile': user_profile,
                   'user_posts': user_posts,
                   'form': form})
    else:
        user_profile = Profile.objects.get_or_create(user=user)[0]
        return render(request, 'accounts/user_profile.html',
                      {'user': user,
                       'user_profile': user_profile,
                       'user_posts': user_posts,
                       'form': form})


@login_required
def view_friends(request):
    user = request.user
    friends = user.friends.all()
    return render(request, 'friends/friends_list.html', {'friends': friends})


@login_required
def add_friend(request):
    if request.method == 'POST':
        form = AddFriendForm(request.POST)
        if form.is_valid():
            friend_username = form.cleaned_data['friend_username']
            friend = User.objects.get(username=friend_username)
            Friend.objects.create(user=request.user, friend=friend)
            # Редирект или другая логика
    else:
        form = AddFriendForm()
    return render(request, 'friends/add_friend.html', {'form': form})


@login_required
def search_friends(request):
    if request.method == 'GET':
        form = SearchFriendsForm(request.GET)
        if form.is_valid():
            search_query = form.cleaned_data['search_query']
            # Логика поиска друзей по search_query
            friends = Friend.objects.filter
            return render(request, 'friends/search_results.html', {'friends': friends})
    else:
        form = SearchFriendsForm()
    return render(request, 'friends/search_friends.html', {'form': form})

