from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth.models import User
from rest_framework import serializers

from accounts.models import Profile


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        """Vérifie si l'email existe"""
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Aucun utilisateur avec cet email.")
        return value

    def send_reset_email(self):
        """Envoie l'email de réinitialisation"""
        email = self.validated_data["email"]
        user = User.objects.get(email=email)
        token = default_token_generator.make_token(user)
        reset_link = f"http://127.0.0.1:8000/api/accounts/reset-password/{user.pk}/{token}/" # A changer lors du déploiement

        send_mail(
            "Réinitialisation de mot de passe",
            f"Cliquez sur ce lien pour réinitialiser votre mot de passe : {reset_link}",
            "admin@mysoul.com",
            [email],
        )

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.profile.role = 'user'  # Assure que personne ne s’inscrit en admin
        user.profile.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)  #  Ajout de l’avatar

    class Meta:
        model = Profile
        fields = ['role', 'avatar', 'is_premium', 'premium_expiration_date']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']
        read_only_fields = ['id', 'username']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile = instance.profile
        profile.avatar = profile_data.get('avatar', profile.avatar)
        profile.save()

        return instance




    
    
