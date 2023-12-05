from rest_framework import serializers
from app1.models import User
from django.utils.encoding import DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,smart_str
from django.core.exceptions import ValidationError
from app1.utils import Util


from django.contrib.auth.tokens import PasswordResetTokenGenerator
class UserRegistrationSerializers(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields = ['email','name','password','password2','tc']
        extra_kwargs ={
            'password':{'write_only':True}
        }
        
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError('password and confirm password does not match')
        return super().validate(attrs)
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class UserLoginSerializer(serializers.ModelSerializer):
     email = serializers.EmailField(max_length =255)
     class Meta:
         model = User
         fields = ['email','password']


class userProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','name']


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255,style={'input_type':'password'},write_only = True)
    password2 = serializers.CharField(max_length=255,style={'input_type':'password'},write_only = True)
    class Meta:
        fields = ['password','password2']
    
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError('password and confirm password does not match')
        user.set_password(password)
        user.save()
        return attrs
    
class SendpasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']
        
    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print(uid)
            token = PasswordResetTokenGenerator().make_token(user)
            link = f'http://127.0.0.1:8000/ResetView/{uid}/{token}'
            print(link)
            attrs['user'] = user  
            attrs['reset_link'] = link 
            # send email
            body = 'Click Following link to reset your password=' +link
            data={
                'email_subject':'reset your password',
                'body':body,
                'to_email':user.email
                
            }
            Util.sendemail(data)
            return attrs
        else:
            raise serializers.ValidationError('You are not a Registered User')

class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255,style={'input_type':'password'},write_only = True)
    password2 = serializers.CharField(max_length=255,style={'input_type':'password'},write_only = True)
    class Meta:
        fields = ['password','password2']
    
    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError('password and confirm password does not match')
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise ValidationError('token is not valid or expired')

            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise ValidationError('token is not valid or expired')
            