from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken


class CookieJWTAuthentication(JWTAuthentication):
    """
    Custom JWT Authentication class that reads tokens from HTTP-only cookies.
    Falls back to Authorization header if cookie is not present.
    """
    
    def authenticate(self, request):
        # First, try to get token from cookie
        cookie_token = request.COOKIES.get('access_token')
        
        if cookie_token:
            # Validate the token from cookie
            validated_token = self.get_validated_token(cookie_token)
            return self.get_user(validated_token), validated_token
        
        # If no cookie, fall back to the default header-based authentication
        return super().authenticate(request)
