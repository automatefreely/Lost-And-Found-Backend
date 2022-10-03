from django.http import JsonResponse
from django.core.paginator import Paginator
from django import forms
from django.forms.models import model_to_dict

from .models import Feedback

USER_EXPERIENCE=(
    ('1','Very Unsatisfied'),('2','Unsatisfied'),('3','Neutral'),('4','Satisfied'),('5','Very Satisfied')
)
class FeedbackForm(forms.Form):
    comment=forms.CharField(max_length=300, required=True)
    user_experience = forms.ChoiceField(choices=USER_EXPERIENCE, required=True)

def newFeedback(req):
    if not req.authenticated:
        return req.unauthorisedResponse

    if req.method != "POST":
        return JsonResponse({"status": False, "error": "Method not allowed"}, status=405)
    
    form = FeedbackForm(req.jsonbody(req))
    if form.is_valid():
        newfeed = Feedback.objects.create(
            user_id = req.user["uid"],
            user_name = req.user["name"],
            comment = form.cleaned_data["comment"],
            user_experience = form.cleaned_data["user_experience"]
        )

        return JsonResponse({
            "status": True,
            "class": "feedback",
            "data": model_to_dict(newfeed)
        }, status=201)
    return JsonResponse({"status": False, "error":"Invalid Form Data"}, status=400)
    

def getFeedbacks(req):
    if req.method != "GET":
        return JsonResponse({"status": False, "error": "Method not allowed"}, status=405)
    
    page_size = req.GET.get("pagesize") 
    page_number = req.GET.get("pagenumber")
    if not page_size:
        page_size = 5
    if not page_number:
        page_number = 1

    feedbacks = Feedback.objects.order_by("-created").values()
    paginated = Paginator(list(feedbacks), page_size)
    curr_page = paginated.get_page(page_number)
    res = {
        "status": True,
        "class": "feedback",
        "data": curr_page.object_list,
        "page_size": len(curr_page.object_list),
        "has_next_page": curr_page.has_next(),
        "next_page_number": curr_page.next_page_number() if curr_page.number < paginated.num_pages else False,
        "total_pages": paginated.num_pages,
        "total_items": paginated.count,
    }
    return JsonResponse(res)
