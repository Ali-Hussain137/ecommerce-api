from rest_framework import serializers
from store_api.models import Product
# from store_api.serializers.image_serializer import ImageSerializer
# from store_api.utility.product_picture import ProductPicture


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'quantity', 'user_id']
    #     depth=1

    # def to_representation(self, instance):
    #     product = super().to_representation(instance)
    #     images = ProductPicture.get_product_pic(product["id"])
    #     serializers_images = ImageSerializer(images, many=True)
    #     product["images"] = serializers_images.data
    #     return product

    
