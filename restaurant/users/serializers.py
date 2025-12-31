from rest_framework import serializers
from users.models import Employee, Customer


class ImageSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['image'] = instance.image.url

        return data

class AccountSerializer(serializers.ModelSerializer):
    pass