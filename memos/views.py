from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .models import Memo

# Create your views here.

class MemoSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    
    class Meta:
        model = Memo
        fields = ['id', 'title', 'content', 'owner_username', 'created_at']

class MemoView(APIView):
    """
    メモビュー - 認証と認可処理を実装
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, memo_id):
        memo = Memo.objects.get(id=memo_id)
        
        # OWASP ASVS V4.1.1, V4.1.3, V4.2.1に沿った認可処理
        # ユーザーが自分のメモにのみアクセス可能
        if memo.owner != request.user:
            return Response(
                {'error': 'このメモにアクセスする権限がありません'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = MemoSerializer(memo)
        return Response(serializer.data)
