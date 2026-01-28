from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
    # Browse unsold items.
    path('', views.index, name='index'),
    # Creta a new listing
    path('new/', views.create, name='create'),
    # Show a particular listing by id
    path('<int:pk>/', views.detail, name='detail'),
    # Edit an existing listing (only for seller)
    path('<int:pk>/edit/', views.edit, name='edit'),
    # Delete a listing (only for seller) - needs to be switched to POST method (currently GET)
    path('<int:pk>/delete/', views.delete, name='delete')
]
