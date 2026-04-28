from rest_framework import serializers
from django.contrib.auth import get_user_model
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

User = get_user_model()
NAME_RE = re.compile(r"[a-zA-Z]+(?:[-'][a-zA-Z]+)*")


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
        trim_whitespace=False,
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password_confirm",
            "first_name",
            "last_name"
        ]

    def validate_username(self, value: str) -> str:
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Имя пользователя обязательно.")

        if len(value) < 3:
            raise serializers.ValidationError(
                "Имя пользователя должно содержать не менее 3 символов."
            )

        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Пользователь с таким именем уже существует")
        return value

    def validate_email(self, value: str) -> str:
        value = value.strip().lower()

        if not value:
            raise serializers.ValidationError("Адрес электронной почты обязателен.")

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует")
        return value

    def validate_first_name(self, value: str | None) -> str | None:
        if value in (None, ""):
            return value

        value = value.strip()

        if not NAME_RE.fullmatch(value):
            raise serializers.ValidationError(
                "Имя должно состоять только из букв алфавита."
            )
        return value

    def validate_last_name(self, value: str | None) -> str | None:
        if value in (None, ""):
            return value

        value = value.strip()

        if not NAME_RE.fullmatch(value):
            raise serializers.ValidationError(
                "Фамилия должна состоять только из букв алфавита."
            )
        return value

    def validate(self, attrs):
        password = attrs.get("password")
        password_confirm = attrs.pop("password_confirm", None)

        if password != password_confirm:
            raise serializers.ValidationError(
                {"password_confirm": "Пароли не совпадают."}
            )

        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError(
                {"password": e.messages},
                code="authorization",
            )
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User.objects.create_user(
            password=password,
            is_staff=False,
            is_active=True,
            **validated_data,
        )

        return user