from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from datetime import timedelta


class TokenDoisDiasAccess(AccessToken):
    lifetime = timedelta(days=2)


class TokenDoisDiasSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return TokenDoisDiasAccess.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        access = self.get_token(self.user)
        data['access'] = str(access)
        return data
