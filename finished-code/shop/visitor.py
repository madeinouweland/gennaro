from shop.models import Product
from shop.models import City

class Visitor:
    def __init__(self, request):
        self.request = request

        if "visitor" not in request.session:
            request.session["visitor"] = {
                "shoppingcart": []  # list of product id's
            }

        self.shopping_cart_product_ids = request.session["visitor"]["shoppingcart"]

    def get_shopping_cart_item_count(self):
        return len(self.shopping_cart_product_ids)

    def add_product_to_shopping_cart(self, product_id):
        self.shopping_cart_product_ids.append(product_id)
        self.request.session.modified = True

    def remove_product_from_shopping_cart(self, product_id):
        self.shopping_cart_product_ids.remove(product_id)
        self.request.session.modified = True

    def get_shopping_cart_items(self):
        products = Product.objects.filter(id__in=self.shopping_cart_product_ids)
        return [{
            "id": p.id,
            "name": p.name,
            "image": p.image,
            "price": p.price,
            "quantity": self.shopping_cart_product_ids.count(p.id)
        } for p in products]

    def shopping_cart_total_price(self):
        return sum([p["price"] * p["quantity"] for p in self.get_shopping_cart_items()])

    def save_delivery_address(self, name, address, city_id):
        self.request.session["visitor"]["deliveryaddress"] = {
            "name": name,
            "address": address,
            "cityid": city_id,
        }
        self.request.session.modified = True

    def get_delivery_details(self):
        delivery_address = self.request.session["visitor"]["deliveryaddress"]
        return {
            "name": delivery_address["name"],
            "address": delivery_address["address"],
            "city": City.objects.get(id=delivery_address["cityid"])
        }

    def has_delivery_address(self):
        return "deliveryaddress" in self.request.session["visitor"]

    def place_order(self):
        # Place the order in the database
        # Send notification emails.
        del self.request.session["visitor"]
