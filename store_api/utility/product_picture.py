from store_api.models import Image


class ProductPicture:
    @classmethod
    def get_product_pic(cls, id):
        image = Image.objects.filter(product_id=id)
        return image