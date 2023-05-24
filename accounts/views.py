from django.views import View
from django.contrib.auth import authenticate, login
from django.http import JsonResponse


class LoginAjaxView(View):

    def post(self, request):

        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return JsonResponse(
                    data={
                        'status': 201
                    },
                    status=200
                )
            return JsonResponse(
                data={
                    'status': 400,
                    'error': 'Пароль и логин не верные'
                },
                status=200
            )
        return JsonResponse(
            data={
                'status': 400,
                'error': 'Введите логин и пароль'
            },
            status=200
        )
