from rest_framework import serializers

from crmApp.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "is_active",
            "is_staff",
            'role',
            'tel',
            'date'
        ]
        extra_kwargs = {"id": {"read_only": True}, "password": {"write_only": True}}

    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        role = validated_data['role']
        first_name = validated_data['first_name']
        tel = validated_data['tel']

        user = User.objects.create(
            username=username,
            email=email,
            role=role,
            first_name=first_name,
            tel=tel
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'first_name', 'tel', 'date']