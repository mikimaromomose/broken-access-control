from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from .models import Memo

# Create your views here.

class MemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memo
        fields = '__all__'

class MemoView(APIView):
    def get(self, request, memo_id):
        memo = Memo.objects.get(id=memo_id)  # 他人のメモにもアクセス可能
        serializer = MemoSerializer(memo)
        return Response(serializer.data)
