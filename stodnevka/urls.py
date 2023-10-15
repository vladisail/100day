from django.contrib import admin
from django.urls import path, include
from main.views import index, course_assignments
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('', index, name='index'),
    path('course_assignments/', course_assignments, name='course_assignments'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)