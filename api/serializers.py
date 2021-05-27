from .models import PropertyAddress, PropertyImage
from user.models import User
from rest_framework import serializers

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone_number', 'image')


class PropertyAddressSerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, required=False)
    user = UserSerializer(required=True)
    class Meta:
        model = PropertyAddress
        fields = ('id', 'city', 'country', 'property_description', 'full_address',
                  'latitude', 'longitude', 'images', 'user')


class CreatePropertyAddressSerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, required=False)
    class Meta:
        model = PropertyAddress
        fields = ('id', 'city', 'country', 'property_description', 'full_address',
                  'latitude', 'longitude', 'images', 'user')