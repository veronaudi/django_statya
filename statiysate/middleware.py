import jwt
from django.conf import settings
from django.http import JsonResponse
from .models import User

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

            try:
                payload = jwt.decode(
                    token,
                    settings.JWT_SECRET_KEY,
                    algorithms=[settings.JWT_ALGORITHM]
                )

                if payload.get("type") != "access":
                    return JsonResponse({"error": "Invalid token type"}, status=401)

                request.user = User.objects.get(id=payload["user_id"])

            except jwt.ExpiredSignatureError:
                return JsonResponse({"error": "Access token expired"}, status=401)
            except Exception:
                return JsonResponse({"error": "Invalid token"}, status=401)

        return self.get_response(request)
