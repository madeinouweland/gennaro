from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template import loader
from shop.models import City
from shop.models import Category
from shop.visitor import Visitor
from django import forms
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse

class DeliveryAddressForm(forms.Form):
    name = forms.CharField(label="Name", max_length=30)
    address = forms.CharField(label="Address", max_length=50)  # street + number
    cities = City.objects.order_by("name")
    choices = [(c.id, f"{c.name} (€{c.delivery_costs:.2f} delivery costs)") for c in cities]
    city = forms.IntegerField(label="City", widget=forms.Select(choices=choices))


class DeliveryAddressView(TemplateView):
    template_name = "shop/deliveryaddress.html"

    def get(self, request):
        visitor = Visitor(request)
        categories = Category.objects.order_by("name")

        if visitor.has_delivery_address():
            form = DeliveryAddressForm(initial={
                "name": visitor.get_delivery_details()["name"],
                "address": visitor.get_delivery_details()["address"],
                "city": visitor.get_delivery_details()["city"].id})
        else:
            form = DeliveryAddressForm()

        context = {
            "visitor": visitor,
            "title": "Delivery address",
            "categories": [{"id": c.id, "name": c.name} for c in categories],
            "form": form,
        }

        template = loader.get_template(self.template_name)
        return HttpResponse(template.render(context, request))

    def post(self, request):
        form = DeliveryAddressForm(request.POST)
        visitor = Visitor(request)
        visitor.save_delivery_address(
            form["name"].value(),
            form["address"].value(),
            form["city"].value())

        if "previous" in request.POST:
            return HttpResponseRedirect(reverse("shoppingcart"))
        else:
            return HttpResponseRedirect(reverse("orderconfirm"))
