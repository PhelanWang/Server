# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from .models import Category, Entry
from .serializers import CategorySerializer, EntrySerializer
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework import permissions


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permissions = (permissions.IsAuthenticatedOrReadOnly,)


def set_response(response):
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET, PUT, DELETE, HEAD, OPTIONS, POST'
    response["Access-Control-Allow-Credentials"] = True
    response["Access-Control-Max-Age"] = '86400'
    response["Access-Control-Allow-Headers"] = "Authorization, Origin, X-Requested-With, Content-Type, Accept"
    return response


def get_headers():
    headers = {'Access-Control-Allow-Origin': '*',
               "Access-Control-Allow-Credentials": "True",
               'Access-Control-Allow-Methods': 'GET, PUT, DELETE, HEAD, OPTIONS, POST',
               'Access-Control-Allow-Headers': "Authorization, Origin, X-Requested-With, Content-Type, Accept",
               }
    return headers

# -------------------------------------------------


class CategoryList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Category.objects.all();
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def options(self, request, *args, **kwargs):
        return Response(headers=get_headers())

    def get_queryset(self):
        user = self.request.user
        print "user : ", user
        return self.queryset.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        return set_response(response)

    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        return set_response(response)


class CategoryDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def options(self, request, *args, **kwargs):
        return Response(headers=get_headers())

    def get(self, request, *args, **kwargs):
        response = self.retrieve(request, *args, **kwargs)
        return set_response(response)

    def put(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)
        return set_response(response)

    def delete(self, request, *args, **kwargs):
        "http DELETE 127.0.0.1:8000/api/categorys/6/"
        # 删除链接必须要加上后面的斜杠,结尾的斜杠 /
        response = self.destroy(request, *args, **kwargs)
        return set_response(response)
# -------------------------------------------------


class EntryList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Entry.objects.all();
    serializer_class = EntrySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def options(self, request, *args, **kwargs):
        return Response(headers=get_headers())

    def get_queryset(self):
        user = self.request.user
        print 'entry user: ', user
        return self.queryset.filter(category_id=self.kwargs['pk'])

    def perform_create(self, serializer):
        print self.request.data
        category = Category.objects.filter(id=self.request.data['category_id'])[0]
        print serializer
        serializer.save(category=category)

    def get(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        return set_response(response)

    def post(self, request, *args, **kwargs):
        print 'POST'
        response = self.create(request, *args, **kwargs)
        return set_response(response)


class EntryDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def options(self, request, *args, **kwargs):
        return Response(headers=get_headers())

    def get(self, request, *args, **kwargs):
        response = self.retrieve(request, *args, **kwargs)
        return set_response(response)

    def put(self, request, *args, **kwargs):
        name = request.data['name']
        phone_number = request.data['phone_number']
        Entry.objects.filter(id=request.data['id']).update(name=name, phone_number=phone_number)
        update_entry = Entry.objects.filter(id=request.data['id'])[0]
        serializer = EntrySerializer(update_entry)
        response = Response(data=serializer.data)
        return set_response(response)

    def delete(self, request, *args, **kwargs):
        response = self.destroy(request, *args, **kwargs)
        return set_response(response)


#------------------------------------------------
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer



from rest_framework_jwt.views import JSONWebTokenAPIView
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime

from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.serializers import (
    JSONWebTokenSerializer)

jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


class MyJSOWebTokenAPIView(JSONWebTokenAPIView):
    serializer_class = JSONWebTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        print "用户登录: ", request.data

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response = Response(response_data)
            response['Access-Control-Allow-Origin'] = '*'
            response["Access-Control-Allow-Headers"] = "Authorization, Origin, X-Requested-With, Content-Type, Accept"
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)