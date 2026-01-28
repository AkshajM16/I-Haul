from django.urls import path
from . import views

app_name = 'conversations'

urlpatterns = [
    # Shows users inbox of conversations
    path('', views.inbox, name='inbox'),

    # Show a single conversation based on id.
    path('<int:pk>/', views.detail, name='detail'),

    # Start a new conversation for a listing
    path('new/<int:listing_pk>/', views.new_conversation, name='new'),
]
