from django import template

def currency_euro(value):
    return f"{value:.2f} €"

def productimage(value):
    return f"https://raw.githubusercontent.com/madeinouweland/gennaroshop/main/products/{value}"

register = template.Library()
register.simple_tag(productimage)

register.filter("currency_euro", currency_euro)  # name of the filter, function
