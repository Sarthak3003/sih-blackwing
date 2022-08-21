
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('query/', include('chatbot.urls')),
    path('bb/', include('bid.urls'))
]
