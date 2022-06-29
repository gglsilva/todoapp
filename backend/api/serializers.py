from asyncore import read
from dataclasses import fields
from rest_framework import serializers
from todo.models import Todo

class TodoSerializer(serializers.ModelSerializer):
    created = serializers.ReadOnlyField()
    completed = serializers.ReadOnlyField()

    class Meta:
        model = Todo
        fields = ['id','title','memo','created','completed']


class TodoToggleCompleteSerializer(serializers.ModelSerializer):
    """
    Não recebe e atualiza nenhum valor dos campos do endpoint, apenas altera para concluído
    """
    class Meta:
        model = Todo
        fields = ['id']
        read_only_fields = ['title', 'memo', 'created', 'completed']    # Especifica campos como somente leitura