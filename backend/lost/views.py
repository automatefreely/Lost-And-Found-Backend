from django.http import JsonResponse
from django.core.paginator import Paginator
from django import forms

from .models import Lost


class NewItemForm(forms.Form):
    title = forms.CharField(max_length=50, strip=True)
    description = forms.CharField(max_length=300, strip=True, required=False)
    location = forms.CharField(max_length=100, required=False, strip=True)
    lostDate = forms.DateTimeField(required=False)
    contactEmail = forms.EmailField(required=False)
    contactPhone = forms.CharField(max_length=10)
    image = forms.URLField(max_length=300, required=False)


selectedCols = [
    "id",
    "user_id",
    "user_name",
    "title",
    "description",
    "created",
    "location",
    "lostDate",
    "contactPhone",
    "contactEmail",
    "image",
    "found"
]

def latestLost(req):
    if(req.method != "GET"):
        return JsonResponse({"status": False, "error": "Method not allowed"}, status=405)

    page_size = req.GET.get("pagesize") 
    page_number = req.GET.get("pagenumber")
    if not page_size:
        page_size = 20
    if not page_number:
        page_number = 1
    lostitems = Lost.objects.filter(found=False).order_by("-created").values(*selectedCols)
    paginated = Paginator(list(lostitems), page_size)
    curr_page = paginated.get_page(page_number)
    
    res = {
        "status": True,
        "class": "lost",
        "data": curr_page.object_list,
        "page_size": len(curr_page.object_list),
        "has_next_page": curr_page.has_next(),
        "next_page_number": curr_page.next_page_number() if curr_page.number < paginated.num_pages else False,
        "total_pages": paginated.num_pages,
        "total_items": paginated.count,
    }

    return JsonResponse(res)
    

def getItem(req, id):
    """
    URI looks like: /lost/<id>
    """
    if req.method != "GET":
        return JsonResponse({"status": False, "error": "Method not allowed"}, status=405)

    item = Lost.objects.filter(id__exact=id).values(*selectedCols).first()
    if item == None:
        return JsonResponse({"status": False, "error": "Item not found"}, status=404)
    return JsonResponse({
        "status": True,
        "class": "lost",
        **item
    })


def newItem(req):
    if not req.authenticated:
        return req.unauthorisedResponse

    if req.method != "POST":
        return JsonResponse({"status": False, "error": "Method not allowed"}, status=405)
    form = NewItemForm(req.jsonbody(req))
    if form.is_valid():
        newLost = Lost.objects.create(
            user_id = req.user["uid"],
            user_name = req.user["name"],
            title = form.cleaned_data["title"],
            description = form.cleaned_data["description"],
            location = form.cleaned_data["location"],
            lostDate = form.cleaned_data["lostDate"],
            contactEmail = form.cleaned_data["contactEmail"],
            contactPhone = form.cleaned_data["contactPhone"],
            image = form.cleaned_data["image"],
        )

        return JsonResponse({
            "status": True,
            "class": "lost",
            "itemId": newLost.id
        }, status = 201)
    return JsonResponse({"status": False, "error":"Invalid Form Data"}, status=400)

def markFound(req):
    if not req.authenticated:
        return req.unauthorisedResponse
    if req.method != "POST":
        return JsonResponse({"status": False, "error": "Method not allowed"}, status=405)

    lostitem = Lost.objects.filter(id = req.jsonbody(req).get("id"), user_id = req.user["uid"]).first()
    if not lostitem:
        return JsonResponse({"status": False, "error": "Item not found"}, status=404)

    lostitem.found = True
    lostitem.save()

    return JsonResponse({
        "status": True
    })

#to get all item from a user 
def getItemOfUser(req , user_id):
    """
    URI looks like: /lost/user/<user_id>
    """
    if req.method != "GET":
        return JsonResponse({"status": False, "error": "Method not allowed"}, status=405)
    item = list(Lost.objects.filter(user_id__iexact = user_id) .all().values(*selectedCols))
    if item == None or len(item)==0:
        return JsonResponse({"status": False, "error": "Items doesnt exist"}, status=404)
    return JsonResponse({
        "status": True,
        "data": item
    })


__all__=[
    "latestLost",
    "getItem",
    "newItem",
    "markFound",
    "getItemOfUser"
]
