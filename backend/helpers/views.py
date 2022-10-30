from PIL import Image
import io
import os
import boto3
from boto3.s3.transfer import S3Transfer
from secrets import token_urlsafe
import pathlib
import jwt
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

from django.http import JsonResponse
from django import forms

from .exceptions import InvalidPassword, ServerError, InvalidUser

# For LDAP auth
# from .ldap_auth import auth

# For aviral auth
from .aviral_auth import auth

# JWT constants and variables

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
tokenHandler = jwt
JWT_SECRET = os.environ.get("JWT_SECRET")

print(JWT_SECRET)

# Amazon S3 constants and variables
s3client = boto3.client(
    's3',
    region_name=os.environ.get("AWS_REGION"),
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_ACCESS_KEY_SECRET"),
)
bucket = os.environ.get("S3_BUCKET_NAME")


def imageUpload(req):
    if not (req.authenticated):
        return req.unauthorisedResponse
    if(req.method=='POST'):
        img_file = req.FILES['image']
        file_ext = pathlib.Path(img_file.name).suffix
        if img_file and (file_ext in ['.jpg', '.png', '.jpeg']) and img_file.size<10485760: #10MB
            img = Image.open(img_file)
            img.thumbnail((1024, 1024)) # Max size of Image allowed -> 1024x1024 pixels
            
            file_to_upload = io.BytesIO()
            img.save(file_to_upload, format=img.format)
            file_to_upload.seek(0)

            filename = req.auth_user["uid"] + '-' + token_urlsafe(10) + file_ext

            s3client.upload_fileobj(
                file_to_upload,
                bucket,
                filename,
                ExtraArgs={'ACL': 'public-read'}
            )
            file_url = 'https://%s.%s/%s' % ( bucket, s3client.meta.endpoint_url[8:], filename)
            file_to_upload.close()
            return JsonResponse({
                "status": True,
                "url": file_url
            }, status=201)
        return JsonResponse({
            "status": False,
            "error": "Invalid Image"
        }, status=400)
    return JsonResponse({"status": False, "error": "Method not allowed"}, status=405)


def authUser(req):
    """
    Authenticated User's LDAP credentials and provides JWT secret in response
    """
    if req.method == "POST":
        form = AuthForm(req.jsonbody(req))
        if form.is_valid():
            try:
                authorised_acc = auth(form.cleaned_data["username"].strip(), form.cleaned_data["password"])
            except InvalidPassword:
                return JsonResponse({"status": False,"error": "Wrong Password"}, status=401)
            except InvalidUser:
                return JsonResponse({"status": False,"error": "Invalid Username"}, status=401)
            except ServerError as e:
                return JsonResponse({"status": False,"error": e.message}, status=500)
            
            msg = {
                "uid"   :   authorised_acc["uid"],
                "name"  :   authorised_acc["name"],
                "expireon"   :   str(datetime.now() + timedelta(days=30))
            }
            jwt_token = tokenHandler.encode(msg, JWT_SECRET, algorithm="HS256")

            return JsonResponse({
                "status": True,
                "secret": jwt_token
            }, status=200)
        return JsonResponse({"status": False, "error":"Invalid Form Data"}, status=400)
    return JsonResponse({"status": False, "error": "Method not allowed"}, status=405)


def getSelfUser(req):
    if not req.authenticated:
        return req.unauthorisedResponse
    if req.method == "GET":
        return JsonResponse({
                "status"    : True,
                "username"  : req.auth_user["uid"],
                "name"      : req.auth_user["name"]
            }, status=200)
    return JsonResponse({"status": False, "error": "Method not allowed"}, status=405)
    