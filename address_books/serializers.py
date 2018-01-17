# coding: utf-8

from rest_framework import serializers
from .models import Category, Entry
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        owner = serializers.ReadOnlyField(source='owner.username')
        fields = ('text', 'date_added', 'id')


class EntrySerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Entry
        category = serializers.ReadOnlyField()
        fields = ('name', 'phone_number', 'date_added', 'category', 'id')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User(
            email = validated_data['email'],
            username = validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()
        return user