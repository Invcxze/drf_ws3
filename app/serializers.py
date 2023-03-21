from rest_framework import serializers
from .models import Product, Cart

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price')

class CartSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Cart
        fields = ('id', 'products', 'total_price')
    def create(self, validated_data):
        products_data = validated_data.pop('products')
        cart = Cart.objects.create(**validated_data)
        for product_data in products_data:
            product = Product.objects.get(id=product_data['id'])
            cart.products.add(product)
        return cart

    def update(self, instance, validated_data):
        products_data = validated_data.pop('products')
        instance.total_price = validated_data.get('total_price', instance.total_price)
        instance.save()
        instance.products.set([])
        for product_data in products_data:
            product = Product.objects.get(id=product_data['id'])
            instance.products.add(product)
        return instance

    def delete(self, instance):
        instance.delete()
