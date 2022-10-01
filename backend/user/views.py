from django.http import HttpResponse, HttpResponseServerError
from django import forms
import jwt
import os
from datetime import datetime, timedelta

from .models import User
from .ldap_auth import auth
from .exceptions import InvalidPassword, ServerError, InvalidUser


class AuthForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=30)


"""
JWT message structure: {
    "uid"   :   "Roll No.",
    "name"  :   "Name",
    "exp"   :   "Expiry Time" // 1 month from creation
}
"""

tokenHandler = jwt.JWT()
JWT_SECRET = os.environ.get("JWT_SECRET")

def auth_user(req):
    """
    Authenticated User's LDAP credentials and provides JWT secret in response
    """
    if req.method == "POST":
        form = AuthForm(req.POST)
        if form.is_valid():
            try:
                authorised_acc = auth(form.cleaned_data["username"].strip(), form.cleaned_data["password"])
            except InvalidPassword:
                return HttpResponse({"status": False,"error": "Wrong Password"}, status=401)
            except InvalidUser:
                return HttpResponse({"status": False,"error": "Invalid Username"}, status=401)
            except ServerError as e:
                return HttpResponseServerError({"status": False,"error": e.message})
            
            try:
                user = User.objects.get(uid__iexact=authorised_acc["uid"])
            except User.DoesNotExist:
                user = User.objects.create(**authorised_acc)
            
            msg = {
                "uid"   :   user.uid,
                "name"  :   user.name,
                "exp"   :   str(datetime.now() + timedelta(days=30))
            }

            jwt_token = tokenHandler.encode(msg, JWT_SECRET, algorithm="HS256")

            return HttpResponse({
                "status": True,
                "secret": jwt_token
            }, status=200)
        return HttpResponse({"status": False, "error":"Invalid Form Data"}, status=400)
    return HttpResponse({"status": False, "error": "Method not allowed"}, status=405)



def get_self(req):
    if req.method == "GET":
        if req.authenticated:
            return HttpResponse({
                "username"  : req.user.uid,
                "name"      : req.user.name,
                "email"     : req.user.mail
            }, status=200)
        return HttpResponse({"status": False, "error": "Unauthorised"}, status=401)
    return HttpResponse({"status": False, "error": "Method not allowed"}, status=405)
    