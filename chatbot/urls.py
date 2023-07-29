from django.urls import path
from .views import ChatbotView, ConversationListView

appname = 'chatbot'

urlpatterns = [
	path('', ChatbotView.as_view(), name='chat'),
    path('list/', ConversationListView.as_view(), name='list')
]