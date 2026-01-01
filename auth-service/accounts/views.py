from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import jwt
import datetime
from django.conf import settings

SECRET_KEY = settings.SECRET_KEY

@csrf_exempt
def register_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        import json
        body = json.loads(request.body)
        username = body.get("username")
        password = body.get("password")

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "User already exists"}, status=400)

        user = User.objects.create_user(username=username, password=password)
        return JsonResponse({"message": "User registered"}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        import json
        body = json.loads(request.body)
        username = body.get("username")
        password = body.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            return JsonResponse({"error": "Invalid credentials"}, status=401)

        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=3),
            "iat": datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return JsonResponse({"token": token}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def user_me(request):
    auth = request.headers.get("Authorization")

    if not auth:
        return JsonResponse({"error": "Authorization header missing"}, status=401)

    try:
        token = auth.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user = User.objects.get(id=payload["id"])
        return JsonResponse({"username": user.username}, status=200)

    except jwt.ExpiredSignatureError:
        return JsonResponse({"error": "Token expired"}, status=401)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=401)
