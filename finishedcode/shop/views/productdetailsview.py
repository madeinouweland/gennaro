from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template import loader
from shop.models import Product
from shop.models import Category
from shop.visitor import Visitor


class ProductDetailsView(TemplateView):
    template_name = "shop/productdetails.html"

    def get(self, request, id):
        visitor = Visitor(request)
        categories = Category.objects.order_by("name")
        product = Product.objects.get(id=id)
        context = {
            "visitor": visitor,
            "categories": [{"id": c.id, "name": c.name} for c in categories],
            "title": product.name,
            "description": product.description,
            "price": product.price,
            "volume": product.volume,
            "image": product.image
        }
        template = loader.get_template(self.template_name)
        return HttpResponse(template.render(context, request))

    def post(self, request, id):
        visitor = Visitor(request)
        visitor.add_product_to_shopping_cart(int(id))
        categories = Category.objects.order_by("name")
        product = Product.objects.get(id=id)
        context = {
            "visitor": visitor,
            "categories": [{"id": c.id, "name": c.name} for c in categories],
            "title": product.name,
            "description": product.description,
            "price": product.price,
            "volume": product.volume,
            "image": product.image
        }
        template = loader.get_template(self.template_name)
        return HttpResponse(template.render(context, request))
