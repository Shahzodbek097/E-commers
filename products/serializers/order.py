from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from products.models import Order, Product


class OrderSerializers(serializers.ModelSerializer):
    umum_narx = serializers.SerializerMethodField()

    class Meta:
        model=Order
        fields=['id', 'product', 'buyurtmachi', 'nechta', 'qachon', 'umum_narx', 'phone_number']

    def get_umum_narx(self, obj):
        return obj.product.narxi * obj.nechta

    def validate_nechta(self, zakas_soni):
        try:
            product_id = self.initial_data['product']
            product=Product.objects.get(id=product_id)

            if zakas_soni>product.ombor:
                raise serializers.ValidationError("Buncha mahsulot omborda yo'q.")

            if zakas_soni < 1:
                raise serializers.ValidationError("Zakaslar kamida 1 ta bo'lishi kerak.")

            return zakas_soni

        except ObjectDoesNotExist:
            raise serializers.ValidationError("Bunday mahsulot yo'q")

    def create(self, validated_data):
        order=Order.objects.create(**validated_data)
        product=order.product
        product.ombor -= order.nechta
        product.save()
        self.send_confirmation_email(order)
        return order

    def send_confirmation_email(self, order):
        print(f"Zakangiz qabul qilindi{order.id}")
