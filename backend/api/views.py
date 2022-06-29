from lib2to3.pgen2 import token
from rest_framework import generics, permissions
from .serializers import TodoSerializer, TodoToggleCompleteSerializer
from todo.models import Todo
from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

# Create your views here.
# Fornece um endpoint somente de leitura
"""
class TodoList(generics.ListAPIView):
    # ListAPIView requer dois atributos obrigatórios, serializer_class e queryset
    # Especificamos TodoSerializer que implementamos anteriormente 
    
    serializer_class = TodoSerializer

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user).order_by('-created')
"""

class TodoListCreate(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes =[permissions.IsAuthenticated] # Apenas usuarios altenticados tem permição para chamar a api

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user).order_by('-created')

    def perform_create(self, serializer):
        #serializador contém um modelo django
        serializer.save(user=self.request.user)


class TodoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # usuário só pode atualizar, excluir posts
        return Todo.objects.filter(user=user)


class TodoToggleComplete(generics.UpdateAPIView):
    serializer_class = TodoToggleCompleteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)

    def perform_update(self, serializer):
        serializer.instance.completed=not(serializer.instance.completed)
        serializer.save()


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request) # analisar o conteúdo da solicitação JSON e retornar um dicionário de dados
            user = User.objects.create_user(
                                            username=data['username'], #Extraímos os valores preenchidos pelo usuário do dicionário
                                            password=data['password']   
                                        )
            user.save() # salvamos o objeto User no banco de dados.
            token = Token.objects.create(user=user) #  criamos o objeto token
            return JsonResponse({'token':str(token)},status=201) # se tudo der certo , retornamos um objeto JsonResponse com um dicionário contendo o token e o código de status 201 indicando a criação bem-sucedida.

        except IntegrityError: # Se houver um erro, retornamos um objeto JsonResponse com um dicionário contendo o erro e o código de status 400 indicando que a solicitação não pode ser atendida.
            return JsonResponse(
                {'error':'username token. choose another username'},
                status=400
            )


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user = authenticate(
                            request,
                            username=data['username'],
                            password=data['password']
                        )
        if user is None:
            return JsonResponse(
                                {'error':'unable to login. ckech username and password'},
                                status=400
                                )                    
        else: # Return user token
            try:
                token = Token.objects.get(user=user)
            except: # if token not in db, create a new one
                token = Token.objects.create(user=user)
            return JsonResponse({'token':str(token)}, status=201)