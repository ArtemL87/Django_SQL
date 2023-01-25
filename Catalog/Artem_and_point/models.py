from django.db import models
from Artem_and_point.resours import POSITIONS, cashier
from datetime import datetime


class Product(models.Model):
    name = models.CharField(max_length = 255, default = "Продукт (товар)")
    price = models.FloatField(default = 0.0)
    composition = models.TextField(default="Состав не указан")


class Staff(models.Model):
    director = 'DI'
    admin = 'AD'
    cook = 'CO'
    cashier = 'CA'
    cleaner = 'CL'

    full_name = models.CharField(max_length = 255, default = "staff")
    position = models.CharField(max_length = 2, choices = POSITIONS, default = cashier)
    labor_contract = models.IntegerField()

    def get_last_name(self):
        return self.full_name.split()[0]



class Order(models.Model):
    time_in = models.DateTimeField(auto_now_add = True) # время заказа
    time_out = models.DateTimeField(null = True) # время закрытия заказа
    cost = models.FloatField(default = 0.0) # стоимость заказа
    pickup = models.BooleanField(default = False)
    complete = models.BooleanField(default = False) # статус заказа
    staff = models.ForeignKey('Staff', on_delete = models.CASCADE)

    products = models.ManyToManyField('Product', through='Product_Order')

    def finish_order(self): # закрытие заказа
        self.time_out = datetime.now()
        self.complete = True
        self.save()

    def get_duration(self):
        if self.complete:
            return f'Время выполнения заказа: {(self.time_out - self.time_in).total_seconds()} секунд'
        else:
            return f'Время прошедшее от начало заказа: {(datetime.now() - self.time_in).total_seconds()} секунд'

class Product_Order(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    in_order = models.ForeignKey(Order, on_delete = models.CASCADE)
    _amount = models.IntegerField(default = 1, db_column='amount')

    def product_amount(self):
        return self.product.price * self._amount

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = int(value) if value >= 0 else 0
        self.save()


'''
class AbstractBaseUser(models.Model):
    password = models.CharField(_('password'), max_length=128)
    last_login = models.DateTimeField(_('last login'), blank=True, null=True)

    is_active = True


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
'''
# Create your models here.
