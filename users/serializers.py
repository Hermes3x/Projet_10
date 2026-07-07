from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'age',
            'can_be_contacted',
            'can_data_be_shared',
        ]

        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_age(self, value):
        if value < 15:
            raise serializers.ValidationError(
                "Un utilisateur doit avoir au moins 15 ans"
            )

        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        # On retire le password des données normales
        password = validated_data.pop('password', None)

        # On met à jour les autres champs normalement (email, age…)
        user = super().update(instance, validated_data)

        # Si un password a été fourni, on le hashe correctement
        if password is not None:
            user.set_password(password)
            user.save()

        return user
