from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template import loader
from shop.models import Category
from shop.visitor import Visitor

class OrderCompletedView(TemplateView):
    template_name = "shop/ordercompleted.html"

    def get(self, request):
        visitor = Visitor(request)
        categories = Category.objects.order_by("name")
        context = {
            "visitor": visitor,
            "title": "Order completed",
            "categories": [{"id": c.id, "name": c.name} for c in categories],
        }
        template = loader.get_template(self.template_name)
        return HttpResponse(template.render(context, request))
