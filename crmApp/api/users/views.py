from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.db.models import Q
from rest_framework.permissions import AllowAny

from crmApp.models import User, AgentSalesProduct
from .serializers import RegistrationSerializer, UserListSerializer


class UserListView(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserListSerializer

    def list(self, request, *args, **kwargs):
        users = User.objects.filter(Q(role='Agent') | Q(role='Menejer'))
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        user = User.objects.get(id=kwargs['pk'])
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        user = User.objects.get(id=kwargs['pk'])
        user.delete()
        return Response({"success": True,
                         "message": f"{status.HTTP_204_NO_CONTENT}"
                         })


class RegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):

        serializer = RegistrationSerializer(data=request.data)

        for user in User.objects.all():
            if not user:
                break
            else:
                try:
                    Token.objects.get(user_id=user.id)
                except Token.DoesNotExist:
                    Token.objects.create(user=user)

        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response(
                {
                    "user": {
                        "id": serializer.data["id"],
                        "username": serializer.data["username"],
                        'familya': serializer.data['first_name'],
                        'tel': serializer.data['tel'],
                        "email": serializer.data["email"],
                        "is_active": serializer.data["is_active"],
                        "is_staff": serializer.data["is_staff"],
                        "role": serializer.data["role"],
                        'qo`shilgan vaqti': serializer.data['date'],
                        "token": token.key,
                    },
                    "status": {
                        "message": "User created",
                        "code": f"{status.HTTP_200_OK} OK",
                    },
                }
            )
        return Response(
             {
                "error": serializer.errors,
                "status": f"{status.HTTP_203_NON_AUTHORITATIVE_INFORMATION}\
                    NON AUTHORITATIVE INFORMATION",
                }
        )


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
        if user is None:
            return Response({
                "ok": False,
                "data": "Login yoki parol hato"
            })
        token, is_create = Token.objects.get_or_create(user=user)
        return Response({
            "success": True,
            "status": status.HTTP_200_OK,
            "message": "ok",
            "user": {
                "id": user.id,
                "username": token.user.username,
                'familya': user.first_name,
                'role': user.role,
                'email': user.email,
                'tel': user.tel,
                'is_staff': user.is_staff,
                "is_active": user.is_active,
                'qo`shilgan_vaqti': user.date,
                "token": token.key,
            },
        })

    def delete(self, request):
        if request.user.is_authenticated:
            request.auth.delete()

            return Response({
                    "ok": True
                })


class AgentSalesProductAmount(APIView):
    def get(self, request, user_id):
        data = AgentSalesProduct.objects.filter(status=True, user=user_id)
        hisob = 0
        for i in data:
            num1 = (i.product.sel_price * i.quantity)
            num2 = (i.product.finish_price * i.quantity)
            foyda = num2-num1
            hisob = hisob + foyda
        return Response({
            "user": user_id,
            "foyda": hisob
        })

    def delete(self, request, user_id):
        data = AgentSalesProduct.objects.filter(status=True, user=user_id)
        data.delete()
        return Response({
            'ok': True
        })
