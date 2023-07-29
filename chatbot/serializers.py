from rest_framework import serializers
from .models import Conversation

class ConversationSerializer(serializers.ModelSerializer):
    question_user_email = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['prompt', 'response', 'question_user_email']

    def get_question_user_email(self, obj):
        return obj.question_user.email