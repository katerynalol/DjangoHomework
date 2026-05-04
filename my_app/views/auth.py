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
