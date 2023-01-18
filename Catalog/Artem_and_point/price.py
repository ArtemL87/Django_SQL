from models import Product

product1 = Product(name = 'Мышка', price = '605.0')
product1.save()

product2 = Product.objects.create(name = 'Монитор', price = '10999.0')