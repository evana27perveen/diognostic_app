from django.contrib.auth.models import Group
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from App_auth.models import CustomUser


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
        )

        user.set_password(validated_data['password'])
        grp_name = self.context.get('group_name')
        user.save()
        group = Group.objects.get_or_create(
            name=grp_name
        )
        group[0].user_set.add(user)
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    username = serializers.EmailField()

    def validate_email(self, value):
        user = CustomUser.objects.filter(username=value).first()
        if not user:
            raise serializers.ValidationError('User not found')
        return value


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128)
    token = serializers.CharField()
    uidb64 = serializers.CharField()

    def validate(self, attrs):
        try:
            uid = urlsafe_base64_decode(attrs['uidb64']).decode()
            print(attrs['token'])
            user = CustomUser.objects.get()
            print(user)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            raise serializers.ValidationError('Invalid reset link')

        if not PasswordResetTokenGenerator().check_token(user, attrs['token']):
            raise serializers.ValidationError('Invalid reset link')

        attrs['user'] = user
        return attrs

    def save(self, **kwargs):
        password = self.validated_data['password']
        self.validated_data['user'].set_password(password)
        self.validated_data['user'].save()
