from django.db import models
from django.db.models import ForeignKey

from account.models import CustomUser, Address
from shop.validators import point_validator, validate_minimum_size


class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    parent = models.ForeignKey("Category", on_delete=models.PROTECT, null=True, blank=True)

    # Product
    def __str__(self):
        return self.title


class Product(models.Model):
    class Tag:
        NEW = 1
        SALE = 2
        OUT_OF_STOCK = 3

    TagTypeChoose = ((Tag.NEW, "new"), (Tag.SALE, "sale"), (Tag.OUT_OF_STOCK, "out of stock"),)
    tag = models.IntegerField(choices=TagTypeChoose, null=True, blank=True)
    cover = models.ImageField(upload_to='uploads/', validators=[validate_minimum_size(400, 600), ])
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    price_after_sale = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return self.title  # carts  # review


class ProductMedia(models.Model):
    product = ForeignKey(Product, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='uploads/')


class Banner(models.Model):
    image = models.ImageField(upload_to='uploads/')
    alt = models.CharField(max_length=250)
    url = models.CharField(max_length=250)
    is_active = models.BooleanField(default=True)
    number = models.IntegerField()


# class review(models.Model):
#     product = OneToOneField(Product, on_delete=models.CASCADE)
#     points = models.DecimalField(max_length=5, decimal_places=2)

class ReviewComment(models.Model):
    review = ForeignKey(Product, on_delete=models.CASCADE, related_name='review')
    text = models.TextField(max_length=255, blank=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    point = models.DecimalField(max_digits=5, decimal_places=2, validators=[point_validator, ])
    date = models.DateField(auto_now=True)


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)


class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="cart")

    def t_price(self):
        t_amount = 0

        for c in self.cart_items.all():
            amount = c.product.price * c.count
            t_amount += amount
        return t_amount

    def __str__(self):
        return self.user.username
    # cart_items


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items")
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    count = models.IntegerField()


class Transaction(models.Model):
    class STATE:
        NEW = 1
        PENDING = 2
        PAYMENT_APPROVED = 3
        PAYMENT_FAILED = 4
        NOT_EXISTS = 5

    TagTypeChoose = ((STATE.NEW, "new"), (STATE.PENDING, "pending"),
                     (STATE.PAYMENT_APPROVED, "payment approved"),
                     (STATE.PAYMENT_FAILED, "payment failed"),
                     (STATE.NOT_EXISTS, "not exist in store")
                     )
    state_payment = models.IntegerField(choices=TagTypeChoose)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name="transaction")
    created = models.DateTimeField(auto_now_add=True)
    send_time = models.DateField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    shipping_price = models.IntegerField()
    total_price = models.IntegerField()


class TransactionItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name="transaction_item")
    count = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
