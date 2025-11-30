from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Item

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'category', 'subcategory', 'name', 'amount']

# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']

#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username = validated_data['username'],
#             email = validated_data['email'],
#             password = validated_data['password']
#         )
#         return user


# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()
    
# class ItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Item
#         fields = ('category', 'subcategory', 'name', 'amount')