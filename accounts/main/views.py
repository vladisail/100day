from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'main/index.html')


def course_assignments(request):
    return render(request, 'main/course_assignments.html')