from django.urls import path
from .views import ChatbotView

appname = 'chatbot'

urlpatterns = [
	path('', ChatbotView.as_view(), name='chat'),
]