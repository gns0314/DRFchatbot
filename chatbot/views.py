from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from dotenv import load_dotenv
from .models import Conversation
from .serializers import ConversationSerializer
import openai
import os

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# 챗봇 뷰
class ChatbotView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user:
            # 사용자당 최대 요청 횟수 (5번으로 설정)
            max_requests_per_user = 5

            # 현재 시간과 마지막 요청 시간 비교
            current_time = timezone.now()
            last_request_time = user.last_request_time
            if (current_time - last_request_time) >= timedelta(days=1):
                # 하루가 지나면 요청 횟수 초기화
                user.request_count = 0

            # 요청 횟수 증가 및 마지막 요청 시간 업데이트
            user.request_count += 1
            user.last_request_time = current_time
            user.save()

            if user.request_count > max_requests_per_user:
                return Response({'error': '일일 사용횟수 5회를 초과했습니다.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

            prompt = request.data
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

                return Response({'response': response}, status=status.HTTP_200_OK)

            return Response({'error': 'No prompt provided.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': 'Unauthorized.'}, status=status.HTTP_401_UNAUTHORIZED)



# 채팅 뷰
class ConversationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        conversations = Conversation.objects.filter(question_user=user)
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)