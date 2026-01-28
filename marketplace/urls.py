from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Homepage
    path('', include('main.urls')),
    # Marketplace items
    path('listings/', include('listings.urls')),
    # User chats
    path('chat/', include('conversations.urls')),
    # Profile
    path('account/', include('account.urls')),
    # Seller dashboard
    path('dashboard/', include('dashboard.urls')),
    # Django admin
    path('admin/', admin.site.urls)
]

# Dev only media serving, will need to use server for production
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
