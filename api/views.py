from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import CustomJWTSerializer

class APILoginView(TokenObtainPairView):
    serializer_class = CustomJWTSerializer
    def post(self, request, *args, **kwargs):
        # 1️⃣ Let SimpleJWT + serializer do authentication & token creation
        response = super().post(request, *args, **kwargs)

        # 2️⃣ Extract tokens from response
        access_token = response.data.get('access')
        refresh_token = response.data.get('refresh')

        # 3️⃣ Set HTTPOnly cookies (INDUSTRY STANDARD)
        response.set_cookie(
            key='bank_access_token',
            value=access_token,
            httponly=True,
            secure=True,      # MUST be True in production (HTTPS)
            samesite='Lax',
            max_age=600       # 10 minutes
        )

        response.set_cookie(
            key='bank_refresh_token',
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite='Lax',
            max_age=86400     # 1 day
        )

        # 4️⃣ Optional but recommended: remove tokens from response body
        # del response.data['access']
        # del response.data['refresh']

        return response


class ProfileAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "username": request.user.username,
            "email": request.user.email
        })
    
class BankApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        return Response(data)