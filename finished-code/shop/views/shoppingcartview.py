from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template import loader
from shop.models import Category
from shop.visitor import Visitor


class ShoppingCartView(TemplateView):
    template_name = "shop/shoppingcart.html"

    def get(self, request):
        visitor = Visitor(request)
        categories = Category.objects.order_by("name")
        context = {
            "visitor": visitor,
            "title": f"Your shopping cart contains {visitor.get_shopping_cart_item_count()} items",
            "categories": [{"id": c.id, "name": c.name} for c in categories],
        }
        template = loader.get_template(self.template_name)
        return HttpResponse(template.render(context, request))

    def post(self, request):
        visitor = Visitor(request)
        categories = Category.objects.order_by("name")

        if "increment" in request.POST:
            visitor.add_product_to_shopping_cart(int(request.POST["increment"]))
        elif "decrement" in request.POST:
            visitor.remove_product_from_shopping_cart(int(request.POST["decrement"]))

        context = {
            "visitor": visitor,
            "title": f"Your shopping cart contains {visitor.get_shopping_cart_item_count()} items",
            "categories": [{"id": c.id, "name": c.name} for c in categories],
        }
        template = loader.get_template(self.template_name)
        return HttpResponse(template.render(context, request))
