import json

from django.views import View
from django.http import HttpResponse, JsonResponse

from .models import User

# Sign Up

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        signed_name = data.get('name', None)
        signed_email = data.get('email', None)
        signed_password = data.get('password', None)
        
        # name, email, password 미입력시 처리 + name/email 이미 존재할 때 처리

        if signed_name == "":
            return JsonResponse({'message':'No username entry'}, status=403)
        
        elif signed_email == "":
            return JsonResponse({'message':'No email entry'}, status=403)
        
        elif signed_password == "":
            return JsonResponse({'message':'No password entry'}, status=403)

        elif User.objects.filter(name=signed_name).exists():
            return JsonResponse({'message':'Already registered username'}, status=403)
        
        elif User.objects.filter(email=signed_email).exists():
            return JsonResponse({'message':'Already registered email'}, status=403)
        else:
            try:  
                User(
                name = signed_name,
                email = signed_email,
                password = signed_password
                ).save()

                return JsonResponse({'message':'SUCCESS'}, status=200)
            except:
                return JsonResponse({'message':'Something is wrong'}, status=400)
    
    def get(self, request):
        return JsonResponse({"MainView is":"Working"}, status=200)

# Log In

class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)
        checked_name = data.get('name', None)   # 데이터 안 넘어올 때 에러 방지 위해 없으면 None 처리
        checked_password = data.get('password', None)

        try:
            if User.objects.filter(name=checked_name).exists():
                user_password = User.objects.get(name=checked_name).password
                if checked_password == user_password:
                    return HttpResponse(status=200)              # 로그인된 뒤에 별도 코멘트 없어도 됨.
                return JsonResponse({"message" : "INVALID_PASSWORD"}, status=401)
        
        except User.DoesNotExist:
            return JsonResponse({"message" : "Username does not exist"}, status=404)
    
    def get(self, request):
        return JsonResponse({"LoginView is":"Working"}, status=200)

