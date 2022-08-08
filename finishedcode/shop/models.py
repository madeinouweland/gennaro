from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.name} ({self.id})"


class Product(models.Model):
    name = models.CharField(max_length=30)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField()
    volume = models.CharField(max_length=10)
    description = models.CharField(max_length=255)
    image = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.name} ({self.id})"


class City(models.Model):
    name = models.CharField(max_length=30)
    delivery_costs = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.id})"
