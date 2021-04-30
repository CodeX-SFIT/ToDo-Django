from django.contrib import auth
from django.http.response import JsonResponse
from django.contrib.auth.models import User
from django.contrib import auth

from rest_framework.views import APIView
from rest_framework import permissions

from .serializers import RegisterSerializer, LoginSerializer, TodoSerializer

from .models import TodoItem

from rest_framework.authentication import SessionAuthentication, BasicAuthentication 

# Create your views here.
class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening
class SignUp(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data = data)
        if serializer.is_valid():
            user = User.objects.create_user(
                data["username"],
                data["email"] if "email" in data else None,
                data["password"],
            )
            return JsonResponse(
                {"success": True, "data": "User Registration Successfull."}, status=201
            )
        else:
            return JsonResponse({"success": False, "error": serializer.errors}, status=400)

class Login(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        data = request.data
        try:
            serializer = LoginSerializer(data=data)
            if serializer.is_valid():
                user = auth.authenticate(username=data['username'],password=data['password'])
                if user is not None:
                    auth.login(request, user)
                    return JsonResponse({"success": True, "data":"Login Successfull."}, status=200)
                else:
                    return JsonResponse({"success": False, "error":"Invalid Credentials."}, status=400)
            else:
                return JsonResponse({"success": False, "error": serializer.errors}, status=400)
        except:
            return JsonResponse({"success": False, "error": "Something Went Wrong!"}, status=500)

class Logout(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request):
        try:
            auth.logout(request)
            return JsonResponse({"success": True, "data": "Logged Out"}, status=200)
        except:
            return JsonResponse({"success": False, "error": "Logout Unsuccessfull"}, status=400)

class TodoList(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request):
        data = request.data
        data['created_by'] = request.user.id
        serializer = TodoSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"success": True, "data": serializer.data}, status=201)
        return JsonResponse({"success": False, "error": serializer.errors}, status=400)
    
    def get(self, request):
        todos = TodoItem.objects.all().filter(created_by = request.user.id).order_by("-created_at")
        serializer = TodoSerializer(todos, many=True)
        return JsonResponse({"success": True, "data": serializer.data}, status = 200)

class TodoDelete(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def delete(self, request, id):
        try:
            todoItem = TodoItem.objects.get(id = id)
        except TodoItem.DoesNotExist:
            return JsonResponse({"success": False, "error":"TodoItem does NOT exist."}, status = 404)

        todoItem.delete()
        return JsonResponse({"success": True, "data":"TodoItem Deleted."}, status = 200)
        
