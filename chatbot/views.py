from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from dotenv import load_dotenv
from .models import Conversation
from .serializers import ConversationSerializer
import openai
import os

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

class ChatbotView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        conversations = request.session.get('conversations', [])
        return Response({'conversations': conversations}, status=status.HTTP_200_OK)

    def post(self, request):

        # 사용자당 최대 요청 횟수 (5번으로 설정)
        max_requests_per_user = 5

        # 사용자 세션에서 요청 횟수 추적
        request_count = request.session.get('request_count', 0)
        if request_count >= max_requests_per_user:
            return Response({'error': '일일 사용횟수 5회를 초과했습니다.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        prompt = request.data.get('prompt')
        if prompt:
            # 이전 대화 기록 가져오기
            session_conversations = request.session.get('conversations', [])
            previous_conversations = "\n".join([f"User: {c['prompt']}\nAI: {c['response']}" for c in session_conversations])
            prompt_with_previous = f"{previous_conversations}\nUser: {prompt}\nAI:"

            model_engine = "text-davinci-003"
            completions = openai.Completion.create(
                engine=model_engine,
                prompt=prompt_with_previous,
                max_tokens=1024,
                n=5,
                stop=None,
                temperature=0.5,
            )
            response = completions.choices[0].text.strip()

            conversation = Conversation(prompt=prompt, response=response, question_user=request.user)
            conversation.save()

            # 대화 기록에 새로운 응답 추가
            session_conversations.append({'prompt': prompt, 'response': response})
            request.session['conversations'] = session_conversations
            request.session.modified = True

            # 요청 횟수 증가
            request.session['request_count'] = request_count + 1
            request.session.modified = True

            return Response({'response': response}, status=status.HTTP_200_OK)

        return Response({'error': 'No prompt provided.'}, status=status.HTTP_400_BAD_REQUEST)


class ConversationListView(APIView):
    def get(self, request):
        conversations = Conversation.objects.all()
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)