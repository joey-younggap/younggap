import json
from django.views import View
from django.http import HttpResponse, JsonResponse

from user.views import login_decorator
from .models import Comment

# Create your views here.

class CommentView(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)

        Comment(
            content = data['content']
        ).save()

        return JsonResponse({'message' : 'SUCCESS'}, status=200)
    
    @login_decorator
    def get(self, request):
        comment_data = Comment.objects.values()
        return JsonResponse({'comments' : list(comment_data)}, status=200)