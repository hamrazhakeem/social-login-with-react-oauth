from .utils import get_id_token
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView

User = get_user_model()

# Create your views here.

class LoginWithGoogle(APIView):
    def post(self, request):
        print('hello')
        if 'code' in request.data:
            code = request.data['code']
            id_token = get_id_token(code)
            
            if 'email' not in id_token:
                return Response({"detail": "Invalid token or missing email"}, status=status.HTTP_400_BAD_REQUEST)
            
            email = id_token['email']
            username = id_token['name']
            first_name = id_token['given_name']
            last_name = id_token['family_name']
     
            user = get_user_or_create(email, username, first_name, last_name)
            
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'role':"user"
            }, status=status.HTTP_200_OK)
        
        return Response({"detail": "Code not provided"}, status=status.HTTP_400_BAD_REQUEST)


def get_user_or_create(email, username, first_name, last_name):
    try:
        user = User.objects.get(email=email)
        if not user.is_active:
            return Response({'error': 'User is blocked'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        user = User.objects.create_user(email=email, username=username, first_name=first_name, last_name=last_name)
    return user