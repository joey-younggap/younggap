import json
from django.views import View
from django.http import HttpResponse, JsonResponse

from user.views import login_decorator
from .models import Comment
from .models import User

# Create your views here.

class CommentView(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        user = User.objects.get(id=request.user.id) 
        # request.user로 전달된 id값과 일치하는 객체 생성

        Comment(
            author = user, # 객체를 author에 담음 (user_id가 담기는 것임)
            content = data['content']
        ).save()

        return JsonResponse({'message' : 'SUCCESS'}, status=200)
    
    @login_decorator
    def get(self, request):
        comment_data = Comment.objects.values()
        return JsonResponse({'comments' : list(comment_data)}, status=200)