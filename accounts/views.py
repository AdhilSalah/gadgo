
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import *
from .email import *


class RegisterAPI(APIView):

    def post(self, request):
        try:
            data = request.data
            serializer = UserSerializer(data=data)

            if serializer.is_valid():
                serializer.save()

                send_otp_via_mail(serializer.data['email'])
                return Response({
                    'status': 200,
                    'message': 'registration success',
                    'data': serializer.data,
                })

            return Response({
                'status': 400,
                'message': 'something went wrong',
                'data': serializer.errors
            })
        except Exception as e:
            print(e)


def signin(request):

    return render(request, 'login.html')


def signup(request):

    return render(request, 'signup.html')
