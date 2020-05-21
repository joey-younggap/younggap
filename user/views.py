import json
import bcrypt
import jwt

from django.views import View
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError

from .models import User



# Sign up => name, password, email 빈 값인데 계정 생성 성공 / 이미 존재하는 name, email이면 예외 처리

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        try:  
            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
                
            User(
                name = data['name'],
                email = data['email'],
                password = hashed_password.decode('utf-8')
            ).save()
            return JsonResponse({'message':'SUCCESS'}, status=200)
        except TypeError:
            return JsonResponse({'message':'INVALID INPUT'}, status=400)
        except KeyError:
            return JsonResponse({'message':'INVALID KEYS'}, status=400)
        except IntegrityError:
            return JsonResponse({'message':'Already registered username'}, status=400)
        except IntegrityError:
            return JsonResponse({'message':'Already registered email'}, status=400)
    
    def get(self, request):
        return JsonResponse({"MainView is":"Working"}, status=200)


# Login => 토큰 발행 성공 / 비번 미입력,불일치 처리 성공 / name 미입력.불일치 시 처리 성공

class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if User.objects.filter(name=data['name']).exists():
                user = User.objects.get(name=data['name'])                
                if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                    token = jwt.encode({'user_id': user.id}, 'secret', algorithm='HS256')
                    return JsonResponse({'token' : token.decode('utf-8')}, status=200)
                return JsonResponse({"message" : "INVALID_PASSWORD"}, status=400)
            else:
                return JsonResponse({"message" : "INVALID_USERNAME"}, status=400)
        
        except KeyError:
            return JsonResponse({"message" : "KeyError"}, status=400) # 키 에러
    
    def get(self, request):
        return JsonResponse({"LoginView is":"Working"}, status=200)


def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):

        try:
            auth_token = request.headers.get('Authorization', None)
            #print('auth_token', auth_token)
            payload = jwt.decode(auth_token, 'secret', algorithm='HS256')
            #print('payload', payload)
            request.user = User.objects.get(id=payload['user_id'])
            return func(self, request, *args, **kwargs)

        except User.DoesNotExist:
            return JsonResponse({"message" : "INVALID_USER"}, status=400)
        except jwt.exceptions.DecodeError:
            return JsonResponse({"message" : "INVALID_TOKEN"}, status=400)
    
    return wrapper

