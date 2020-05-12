import json

from django.views import View
from django.http import HttpResponse, JsonResponse

from .models import Comment

# Create your views here.

class CommentView(View):
    def post(self, request):
        data = json.loads(request.body)
        author = User.objects.get(name=data['name'])  # 이건 오버스펙. 이건 당연히 들어오는 값이어야 함. 

        Comment(
            content = data['content']
        ).save()

        return JsonResponse({'message' : 'SUCCESS'}, status=200)
    
    def get(self, request):
        comment_data = Comment.objects.values()
        return JsonResponse({'comments' : list(comment_data)}, status=200)