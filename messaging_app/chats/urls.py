from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet

# DRF router setup
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

# URLs generated from the router
urlpatterns = [
    path('', include(router.urls)),
]
