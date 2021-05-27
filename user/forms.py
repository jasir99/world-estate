from rest_framework import serializers
from .models import User


class EmailValidator(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)

    def validate(self, attrs):
        email = attrs.get('email')
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return True
        raise serializers.ValidationError('Email already in use')


class UserNameValidator(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

    def validate(self, attrs):
        username = attrs.get('username')
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return True
        raise serializers.ValidationError('Username already in use')


class PhoneValidator(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone_number',)

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        try:
            User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return True
        raise serializers.ValidationError('Phone number already in use')
