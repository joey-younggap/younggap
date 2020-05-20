import json
import bcrypt
import jwt

from django.views import View
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError

from .models import User


# Sign Up 1안 : 완전
# => name, email, password 반 값일 때, name/email 존재 시 모두 다 if문으로 예외 처리

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        signed_name = data.get('name', None)
        signed_email = data.get('email', None)
        signed_password = data.get('password', None)
        
        # name, email, password 미입력시 처리 + name/email 이미 존재할 때 처리

        if signed_name == "":
            return JsonResponse({'message':'No username entry'}, status=400)
        
        elif signed_email == "":
            return JsonResponse({'message':'No email entry'}, status=400)
        
        elif signed_password == "":
            return JsonResponse({'message':'No password entry'}, status=400)

        elif User.objects.filter(name=signed_name).exists():
            return JsonResponse({'message':'Already registered username'}, status=400)
        
        elif User.objects.filter(email=signed_email).exists():
            return JsonResponse({'message':'Already registered email'}, status=400)
        else:
            try:  
                hashed_password = bcrypt.hashpw(signed_password.encode('utf-8'), bcrypt.gensalt())
                
                User(
                name = signed_name,
                email = signed_email,
                password = hashed_password.decode('utf-8')
                ).save()

                return JsonResponse({'message':'SUCCESS'}, status=200)
            except:
                return JsonResponse({'message':'Something is wrong'}, status=400)
    
    def get(self, request):
        return JsonResponse({"LoginView is":"Working"}, status=200)


# Sign up 2안 : 불완전
# => name, password, email 빈 값인데 계정 생성 성공 / 이미 존재하는 name, email이면 예외 처리

# class SignUpView(View):
#     def post(self, request):
#         data = json.loads(request.body)
        
#         try:  
#             hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
                
#             User(
#                 name = data['name'],
#                 email = data['email'],
#                 password = hashed_password.decode('utf-8')
#             ).save()
#             return JsonResponse({'message':'SUCCESS'}, status=200)
#         except TypeError:
#             return JsonResponse({'message':'INVALID INPUT'}, status=400)
#         except KeyError:
#             return JsonResponse({'message':'INVALID KEYS'}, status=400)
#         except IntegrityError:
#             return JsonResponse({'message':'Already registered username'}, status=400)
#         except IntegrityError:
#             return JsonResponse({'message':'Already registered email'}, status=400)
    
#     def get(self, request):
#         return JsonResponse({"MainView is":"Working"}, status=200)



# Log In 1안 : name/password 미입력 시 if문 처리 / name, password 불일치 시 처리 

# class LoginView(View):
#     def post(self, request):
#         data = json.loads(request.body)

#         # name, pass 미입력, name 존재하지 않을 시 처리 후 진행
#         try:
            
#             if data['name'] == '':
#                 return JsonResponse({"message" : "Please enter username"}, status=400)
#             elif data['password'] == '':
#                 return JsonResponse({"message" : "Please enter password"}, status=400)

#             if User.objects.filter(name=data['name']).exists():
#                 user = User.objects.get(name=data['name'])                
#                 if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
#                     token = jwt.encode({'user_id': user.id}, 'secret', algorithm='HS256')
#                     return JsonResponse({'token' : token.decode('utf-8')}, status=200)
#                 return JsonResponse({"message" : "INVALID_PASSWORD"}, status=400)
#             else:
#                 return JsonResponse({"message" : "INVALID_USERNAME"}, status=400)
            
#         except User.DoesNotExist:
#             return JsonResponse({"message" : "Username does not exist"}, status=404)
    
#     def get(self, request):
#         return JsonResponse({"LoginView is":"Working"}, status=200)


# Login 2안 : 해당 name 가진 유저가 존재하고, 비밀번호 일치하면 토큰 발행 / 유저 없으면 에러 발생
#  ==> 토큰 발행 성공 / 비번 미입력,불일치 처리 성공 / name 미입력.불일치 시 처리 성공

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
        
        except User.DoesNotExist:
            return JsonResponse({"message" : "Username does not exist"}, status=404)
    
    def get(self, request):
        return JsonResponse({"LoginView is":"Working"}, status=200)


def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):

        try:
            auth_token = request.headers.get('Authorization', None)
            print('auth_token', auth_token)
            payload = jwt.decode(auth_token, 'secret', algorithm='HS256')
            print('payload', payload)
            request.user = User.objects.get(id=payload['user_id'])
            return func(self, request, *args, **kwargs)

        except User.DoesNotExist:
            return JsonResponse({"message" : "INVALID_USER"}, status=400)
        except jwt.exceptions.DecodeError:
            return JsonResponse({"message" : "INVALID_TOKEN"}, status=400)
    
    return wrapper

