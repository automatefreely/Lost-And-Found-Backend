from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import F

from .models import Lost

def latestLost(req):
    if(req.method == "GET"):
        page_size = req.GET.get("pagesize") 
        page_number = req.GET.get("pagenumber")
        if not page_size:
            page_size = 20
        if not page_number:
            page_number = 1
        lostitems = Lost.objects.filter(
                found=False
            ).select_related().order_by(
                "-created"
            ).annotate(
                user_id = F("user__uid"),
                user_name = F("user__name")
            ).values(
                "id",
                "user_uid",
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
            )
        paginated = Paginator(lostitems, page_size)
        curr_page = paginated.get_page(page_number)
        
        res = {
            "data": curr_page.object_list,
            "page_size": len(curr_page.object_list),
            "has_next_page": curr_page.has_next(),
            "next_page_number": curr_page.next_page_number() if curr_page.number < paginated.num_pages else False,
            "total_pages": paginated.num_pages,
            "total_items": paginated.count,
        }

        return HttpResponse(res)
