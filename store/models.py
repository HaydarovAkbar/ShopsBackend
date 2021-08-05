from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.user.__str__()
# def create_user(sender,instance)


class Categories(models.Model):
    category_name = models.CharField(max_length = 200,null=False)
    description = models.CharField(max_length=300,null=True)
    def __str__(self):
        return self.category_name
class Products(models.Model):
    category = models.ForeignKey(Categories,on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200,null=False)
    price = models.FloatField(null=False)
    image = models.ImageField(null=True)
    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return ''
    def __str__(self):
        return self.product_name
class Orders(models.Model):
    customer = models.ForeignKey(Customer, on_delete= models.CASCADE,null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.id)
class Order_details(models.Model):
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    order = models.ForeignKey(Orders,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0,null=True)
    @property
    def total(self):
        return self.quantity * self.product.price


