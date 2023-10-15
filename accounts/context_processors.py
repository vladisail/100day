def current_user(request):
    if request.user.is_authenticated:
        return {'current_user': request.user}
    return {'current_user': None}