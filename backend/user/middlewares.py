from datetime import datetime
import os
from dotenv import load_dotenv
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
import jwt
load_dotenv()

from .models import User

tokenHandler = jwt.JWT()
JWT_SECRET = os.environ.get("JWT_SECRET")

class BasicMiddleware:
    """
    request.user = user || None,
    request.authenticated = True || False,
    request.unauthorisedResponse = Unauthorised User error Response (status code = 401)
    adds a request.user, req.authenticated for making authenticated routes easy
    also adds req.unauthorisedResponse for unauthenticated ROutes error Response
    JWT secret is provided in the HTTP Request Headers under the key "secret"
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.unauthorisedResponse = HttpResponse({"error":"User authentication required"}, status=401)

        if (request.headers["secret"] and request.headers["secret"]!=""):
            message = tokenHandler.decode(request.headers["secret"], JWT_SECRET, algorithms="HS256")
            try:
                user = User.objects.get(uid__exact=message["uid"])
            except User.DoesNotExist:
                user = None

            request.user = user
            if (user!=None and datetime.fromisoformat(message["exp"]) > datetime.now()) :
                request.authenticated = True
            else:
                request.authenticated = False
        else:
            request.user = None
            request.authenticated = False
        response = self.get_response(request)
        return response