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

    def to_representation(self, instance):
        # La sortie JSON normale (avec tous les champs sauf password)
        representation = super().to_representation(instance)

        request = self.context.get('request')

        # Si on regarde le profil d'un AUTRE utilisateur → on masque ses données perso
        if request and request.user.is_authenticated and instance != request.user:
            champs_prives = [
                'first_name', 'last_name', 'email',
                'age', 'can_be_contacted', 'can_data_be_shared',
            ]
            for champ in champs_prives:
                representation.pop(champ, None)

        return representation
