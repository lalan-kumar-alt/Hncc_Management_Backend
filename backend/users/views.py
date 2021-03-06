from django.db.models.query import QuerySet
from .models import NewUser, Profile
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer, ProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics


class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class Users_year(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        querySet = NewUser.objects.all()
        year = self.request.query_params.get('year')
        if year is not None:
            querySet = querySet.filter(year=year)
        return querySet


class User_profile(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        querySet = Profile.objects.all()
        user = self.request.user
        if user is not None:
            querySet = querySet.filter(user=user)
        return querySet


class Other_user_profiles(generics.ListAPIView):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        id = self.kwargs['pk']
        return Profile.objects.filter(id=id)
