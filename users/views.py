# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import jwt
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from rest_framework import exceptions, permissions, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from address_books.serializers import UserSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


class CreateUserView(CreateAPIView):
    model = User.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        user = self.model.get(username=serializer.data['username'])
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.is_staff = True
        headers['Access-Control-Allow-Origin'] = '*'
        return Response(
            {
                'confirmation_url': reverse(
                    'activate-user', args=[token], request=request
                )
            },
            status=status.HTTP_201_CREATED, headers=headers
        )


class ActivateUser(APIView):
    def get(self, request, *args, **kwargs):
        token = kwargs.pop('token')
        print token
        try:
            payload = jwt_decode_handler(token)
        except jwt.ExpiredSignature:
            msg = _('Signature has expired.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = _('Error decoding signature.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()

        user_to_activate = User.objects.get(id=payload.get('user_id'))
        user_to_activate.is_active = True
        user_to_activate.save()
        return Response(
            {'User Activated'},
            status=status.HTTP_200_OK,headers={"Access-Control-Allow-Origin": "*"}
        )