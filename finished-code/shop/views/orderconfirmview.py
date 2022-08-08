from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from shop.models import Category
from shop.visitor import Visitor

class OrderConfirmView(TemplateView):
    template_name = "shop/orderconfirm.html"

    def get(self, request):
        visitor = Visitor(request)
        categories = Category.objects.order_by("name")
        context = {
            "visitor": visitor,
            "title": "Confirm your order",
            "categories": [{"id": c.id, "name": c.name} for c in categories],
            "total_costs": visitor.shopping_cart_total_price() + visitor.get_delivery_details()["city"].delivery_costs,
        }
        template = loader.get_template(self.template_name)
        return HttpResponse(template.render(context, request))

    def post(self, request):
        if "previous" in request.POST:
            return HttpResponseRedirect(reverse("deliveryaddress"))
        else:
            visitor = Visitor(request)
            visitor.place_order()
            return HttpResponseRedirect(reverse("ordercompleted"))
