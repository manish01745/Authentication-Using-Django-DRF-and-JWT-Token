from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from app1.serializers import UserRegistrationSerializers,UserLoginSerializer,userProfileSerializer,UserChangePasswordSerializer,SendpasswordResetEmailSerializer,UserPasswordResetSerializer
from django.contrib.auth import authenticate
from app1.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# generated token
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,format=None):
        serialiazer = UserRegistrationSerializers(data=request.data)
        if serialiazer.is_valid(raise_exception=True):
            user = serialiazer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token,'msg':'registration successful'},status=status.HTTP_201_CREATED)
        return Response(serialiazer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email,password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token,'msg':'login successful'},status=status.HTTP_200_OK)
            else:
                return Response({'errors':{"non_field_errors:[Email or password is not valid']"}},status=status.HTTP_404_NOT_FOUND)
        
class UserProfileView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes =[IsAuthenticated]
    def get(self,request,format=None):
        serializer = userProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)

class UserChangePasswordView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes =[IsAuthenticated]
    def get(self,request,format=None):
        serializer = UserChangePasswordSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'password change succesfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
    
class SendpasswordResetEmailView(APIView):
       renderer_classes=[UserRenderer]
       def post(self,request,format=None):
         serializer = SendpasswordResetEmailSerializer(data=request.data)
         if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password reset link send Please check your email'},status=status.HTTP_200_OK)
         return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)


class UserPasswordResetView(APIView):    
    renderer_classes=[UserRenderer]
    def post(self,request,uid,token,format=None):
        serializer = UserPasswordResetSerializer(data=request.data,context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password reset successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)