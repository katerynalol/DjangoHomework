from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from rest_framework_simplejwt.exceptions import TokenError

from my_app.serializers import UserRegistrationSerializer, UserLoginSerializer
from my_app.utils import set_jwt_cookies, REFRESH_COOKIE_NAME, clear_jwt_cookies
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )

        return response


class LoginUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request, *args, **kwargs) -> Response:
        data = request.data

        serializer = UserLoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        try:
            response = Response(
                status=status.HTTP_200_OK,
            )

            set_jwt_cookies(response=response, user=user)

            return response

        except Exception as e:
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={
                    "message": str(e)
                }
            )


class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token') or request.data.get('refresh')

        if not refresh_token:
            return Response({
                'error': 'Refresh токен обязателен'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = refresh.access_token

            response = Response({
                'message': 'Токен успешно обновлен'
            }, status=status.HTTP_200_OK)

            from my_app.utils import set_access_cookie
            set_access_cookie(response, str(access_token))

            return response

        except Exception as e:
            return Response({
                'error': 'Неверный refresh токен'
            }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, *args, **kwargs) -> Response:
        try:
            refresh_token = request.COOKIES.get(REFRESH_COOKIE_NAME)

            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

        except TokenError:
            pass

        except Exception as e:
            return Response(
                data={
                    "message": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        response = Response(
            status=status.HTTP_200_OK,
        )

        clear_jwt_cookies(response=response)

        return response


