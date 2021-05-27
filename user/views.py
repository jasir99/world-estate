from django.http import JsonResponse
from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken, APIView

from .forms import EmailValidator, PhoneValidator
from .models import UserReview, User
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer,ResetPasswordEmailRequestSerializer, UserReviewSerializer

'''
  A class for registering users
'''

class ValidateAPI(APIView):
    def post(self, request, format='json'):
        if 'email' in request.data:
            validate_class = EmailValidator(data=request.data)
        else:
            validate_class = PhoneValidator(data=request.data)
        validate_class.is_valid(raise_exception=True)
        return JsonResponse({ 'msg': request.data}, status=200)


class RegisterAPI(APIView):
    def post(self, request, format='json'):
        if 'is_staff' in request.data and request.data['is_staff'] or 'is_superuser' in request.data and request.data['is_superuser']:
            return JsonResponse({'status': False, 'msg': 'Unautorized request', 'data': {}}, status=200)
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user:
            token = Token.objects.create(user=user)
            data = {
                'token': token.key,
                'user': {
                    'userId': user.pk,
                    'username': user.username,
                    'email': user.email,
                    'phone_number': user.phone_number,
                },
            }
            return JsonResponse({'status': True, 'msg': 'Succesfully created user', 'data': data}, status=200)
        return JsonResponse({'status': False, 'msg': 'Could not create user', 'data': {}}, status=400)


'''
  A class for login user
'''

class LoginAPI(ObtainAuthToken):
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        properties = serializer.validated_data['properties']
        if user:
            token, create = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'user': {
                    'userId': user.pk,
                    'username': user.username,
                    'email': user.email,
                    'phone_number': user.phone_number,
                    'properties': properties
                },
            }
            return JsonResponse({'status': True, 'msg': 'Succesfully logged in user', 'data': data}, status=200)
        return JsonResponse({'status': False, 'msg': 'Username or Password is incorect', 'data': {}}, status=401)


'''
  A class for logout user
'''

class LogOutAPI(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request, format=None):
        try:
            request.user.auth_token.delete()
        except (AttributeError):
            pass

        return JsonResponse({'status': True, 'msg': 'Successfully logged out'}, status=200)


'''
  A class for retrieving authenticated user
'''

class UserAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class RequestPasswordResetEmailAPI(APIView):
  def post(self,request,*args,**kwargs):
    serializer = ResetPasswordEmailRequestSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data
        token, create = Token.objects.get_or_create(user=user)
        return JsonResponse({ 'status': True, 'data': token.key, 'msg': 'We have sent you a link to reset your password!' }, status=200)
    return JsonResponse({'status': False, 'msg': 'No registered user with this email!'}, status=400)


class SetNewPassword(APIView):
    def post(self, request):
        user = self.request.user
        if not user.is_anonymous:
            password = request.data['password']
            user.set_password(password)
            user.save()
            request.user.auth_token.delete()
            return JsonResponse({'status': True, 'msg': 'Password changed'}, status=200)
        return JsonResponse({'status': False, 'msg':'No token was provided'}, status=401)


class RetrieveUserAPI(APIView):
    def get_queryset(self, pk):
        if pk is None:
            self.queryset = User.objects.all()
        else:
            self.queryset = User.objects.filter(id=pk)

    def get(self, request, pk=None):
        self.get_queryset(pk)
        serializer = UserSerializer(self.queryset, many=True)
        return JsonResponse(
            {'status': True, 'msg': 'Succesfully retrived categories', 'data': serializer.data})


class UserReviewAPI(APIView):
    def get_queryset(self, pk):
        if pk is None:
            self.queryset = UserReview.objects.all()
        else:
            self.queryset = UserReview.objects.filter(reviewedUser=pk)

    def get(self, request, pk=None):
        self.get_queryset(pk)
        review_serializer_class = UserReviewSerializer(self.queryset, many=True)
        return JsonResponse(
            {'status': True, 'msg': 'Succesfully retrived categories', 'data': review_serializer_class.data})


    def post(self, request):
        user = self.request.user

        data = request.data
        data['reviewingUser'] = user.id

        review_serializer_class = UserReviewSerializer(data=data)

        review_serializer_class.is_valid(raise_exception=True)
        review = review_serializer_class.save()
        if review:
            data = {
                'review': {
                    'id': review.pk,
                    'reviewedUser': review.reviewedUser.pk,
                    'reviewingUser': review.reviewingUser.pk,
                    'content': review.content,
                    'rating': review.rating,
                },
            }
            return JsonResponse({'status': True, 'data': data}, status=200)
        return JsonResponse({'status': False, 'data': review_serializer_class.errors}, status=400)
