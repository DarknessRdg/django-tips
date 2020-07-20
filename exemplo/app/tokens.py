from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenObtainPairSerializer
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


class TokenTresDiasRefresh(RefreshToken):
    """
    Token de refresh com 3 dias de duração, com um token de acesso
    com 2 dias de duração.
    """
    lifetime = timedelta(days=3)

    @property
    def access_token(self):
        """
        Retorna um token de acesso com 2 dias de duração
        """
        access = TokenDoisDiasAccess()

        # Use instantiation time of refresh token as relative timestamp for
        # access token "exp" claim.  This ensures that both a refresh and
        # access token expire relative to the same time if they are created as
        # a pair.
        access.set_exp(from_time=self.current_time)

        no_copy = self.no_copy_claims
        for claim, value in self.payload.items():
            if claim in no_copy:
                continue
            access[claim] = value

        return access


class TokenAccessRefreshSerializer(TokenObtainPairSerializer):
    """
    Serializer para criar tokens de `access` e `refresh`.
    """
    def get_token(cls, user):
        """
        Sobrecreve a criação padrão to token de refresh.
        """
        return TokenTresDiasRefresh.for_user(user)

