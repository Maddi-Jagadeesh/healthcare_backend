# healthcare_backend/urls.py

from django.contrib import admin
from django.urls import path, include  # Make sure 'include' is imported

urlpatterns = [
    path('admin/', admin.site.urls),
    # This line is essential. It tells Django that any URL starting
    # with 'api/' should be handled by the 'api.urls' file.
    path('api/', include('api.urls')),
]