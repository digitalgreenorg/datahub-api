from django.db import models
from django.db.models import fields
from accounts.models import User
from rest_framework import serializers

class UserCreateSerializer(serializers.ModelSerializer):
    """UserCreateSerializer"""

    class Meta:
        model = User
        # fields = (
        #     "email",
        #     "first_name",
        #     "last_name",
        #     "phone_number",
        #     "role",
        #     "status",
        #     "subscription"
        #     )
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "role",
            "status",
            "subscription",
            "profile_picture"
        )

class UserUpdateSerializer(serializers.ModelSerializer):
    """UserUpdateSerializer"""

    class Meta:
        model = User
        exclude = ("created_at", "updated_at")
