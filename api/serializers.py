from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from Admin.models import Admin

class CustomJWTSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # return token
        # check if user is admin
        try:
            admin = Admin.objects.get(username=user.username)
            if admin.check_password(user.password):  # Verify Argon2 hashed password
                # Add custom claims
                token['username'] = user.username
                token['email'] = user.email
                token['is_staff'] = user.is_staff
                token['admin_role'] = admin.role  # Add admin role to the token
        except Admin.DoesNotExist:
            # return unautohrized user response 
            pass
            
        # Custom payload
        # token['username'] = user.username
        # token['email'] = user.email
        # token['is_staff'] = user.is_staff
        print(f"Generated token for user {user.username}: {token}")
        return token
