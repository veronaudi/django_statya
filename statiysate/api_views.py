from django.http import JsonResponse
from .models import Article
from .models import Comment
from django.views.decorators.csrf import csrf_exempt
import json
from .jwt_utils import create_access_token, create_refresh_token
from .jwt_utils import decode_token
import jwt
from django.contrib.auth import get_user_model

def api_article_list(request):
    articles = Article.objects.all().values("id", "title", "short_description", "category", "created_at")
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Unauthorized"}, status=401)
    return JsonResponse(list(articles), safe=False)


def api_article_detail(request, id):
    try:
        article = Article.objects.values("id", "title", "short_description", "text", "category", "created_at", "user_id").get(id=id)
        return JsonResponse(article)
    except Article.DoesNotExist:
        return JsonResponse({"error": "Статьи нет!"}, status=404)

@csrf_exempt  #отключение защиты
def api_create_article(request):
    if request.method != "POST":
        return JsonResponse({"error": "Use POST"}, status=405)

    data = json.loads(request.body)
    required = ["title", "short_description", "text", "category", "user_id"]
    for field in required:
        if field not in data:
            return JsonResponse({"error": f"Нет поля: {field}"}, status=400)

    article = Article.objects.create(
        title=data["title"],
        short_description=data["short_description"],
        text=data["text"],
        category=data["category"],
        user_id=data["user_id"]
    )
    return JsonResponse({"id": article.id}, status=201)


@csrf_exempt
def api_update_article(request, id):
    if request.method != "PUT":
        return JsonResponse({"error": "Use PUT"}, status=405)
    data = json.loads(request.body)
    try:
        article = Article.objects.get(id=id)
    except Article.DoesNotExist:
        return JsonResponse({"error": "Нет статьи"}, status=404)

    #обновляем поля
    for field in ["title", "short_description", "text", "category"]:
        if field in data:
            setattr(article, field, data[field]) #присваивает значения динамически
    article.save()
    return JsonResponse({"status": "updated"})


@csrf_exempt
def api_delete_article(request, id):
    if request.method != "DELETE":
        return JsonResponse({"error": "Use DELETE"}, status=405)

    try:
        article = Article.objects.get(id=id)
    except Article.DoesNotExist:
        return JsonResponse({"error": "Статьи нет!"}, status=404)

    article.delete()
    return JsonResponse({"status": "deleted"})

def api_articles_by_category(request, category):
    articles = Article.objects.filter(category=category).values(
        "id",
        "title",
        "short_description",
        "category",
        "created_at"
    )
    return JsonResponse(list(articles), safe=False)

def api_articles_sorted_by_date(request):
    articles = Article.objects.all().order_by("-created_at").values(
        "id",
        "title",
        "short_description",
        "category",
        "created_at"
    )
    return JsonResponse(list(articles), safe=False)

def comment_list(request):
    comments = Comment.objects.all().values(
        "id", "article_id", "author_name", "text", "date"
    )
    return JsonResponse(list(comments), safe=False)

def comment_detail(request, id):
    try:
        comment = Comment.objects.values(
            "id", "article_id", "author_name", "text", "date"
        ).get(id=id)
        return JsonResponse(comment)
    except Comment.DoesNotExist:
        return JsonResponse({"error": "Коммента нет!"}, status=404)

@csrf_exempt
def comment_create(request):
    if request.method != "POST":
        return JsonResponse({"error": "Use POST"}, status=405)

    data = json.loads(request.body)
    required = ["article_id", "author_name", "text"]
    for field in required:
        if field not in data or not data[field]:
            return JsonResponse({"error": f"Отсутствует:'{field}'"}, status=400)

    try:
        article = Article.objects.get(id=data["article_id"])
    except Article.DoesNotExist:
        return JsonResponse({"error": "Статья не найдена!"}, status=404)

    comment = Comment.objects.create(
        article=article,
        author_name=data["author_name"],
        text=data["text"],
    )
    return JsonResponse({"message": "Коммент создан", "id": comment.id}, status=201)

@csrf_exempt
def comment_update(request, id):
    if request.method != "PUT":
        return JsonResponse({"error": "Use PUT"}, status=405)

    try:
        comment = Comment.objects.get(id=id)
    except Comment.DoesNotExist:
        return JsonResponse({"error": "Комментария нет."}, status=404)

    data = json.loads(request.body)

    if "author_name" in data:
        if not data["author_name"]:
            return JsonResponse({"error": "author_name cannot be empty"}, status=400)
        comment.author_name = data["author_name"]

    if "text" in data:
        if not data["text"]:
            return JsonResponse({"error": "text cannot be empty"}, status=400)
        comment.text = data["text"]

    comment.save()
    return JsonResponse({"message": "Коммент обновлен"})

@csrf_exempt
def comment_delete(request, id):
    if request.method != "DELETE":
        return JsonResponse({"error": "Use DELETE"}, status=405)

    try:
        comment = Comment.objects.get(id=id)
    except Comment.DoesNotExist:
        return JsonResponse({"error": "Коммент не найден!"}, status=404)

    comment.delete()
    return JsonResponse({"message": "Коммент удален"})

@csrf_exempt
def token_obtain(request):
    if request.method != "POST":
        return JsonResponse({"error": "Use POST"}, status=405)

    data = json.loads(request.body)
    name = data.get("name")
    password = data.get("password")
    #user = authenticate(name=name, password=password)
    User = get_user_model()

    try:
        user = User.objects.get(name=name)
    except User.DoesNotExist:
        return JsonResponse({"error": "Invalid credentials"}, status=401)
    if not user:
        return JsonResponse({"error": "Invalid credentials"}, status=401)

    return JsonResponse({
        "access": create_access_token(user.id),
        "refresh": create_refresh_token(user.id)
    })


@csrf_exempt
def token_refresh(request):
    if request.method != "POST":
        return JsonResponse({"error": "Use POST"}, status=405)

    data = json.loads(request.body)
    refresh = data.get("refresh")

    try:
        payload = decode_token(refresh)
        if payload["type"] != "refresh":
            return JsonResponse({"error": "Invalid token type"}, status=401)

        new_access = create_access_token(payload["user_id"])
        return JsonResponse({"access": new_access})

    except jwt.ExpiredSignatureError:
        return JsonResponse({"error": "Refresh token expired"}, status=401)

    except jwt.InvalidTokenError:
        return JsonResponse({"error": "Invalid token"}, status=401)

