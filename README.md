# Broken Access Control Demo

このプロジェクトは、OWASP Top 10の「Broken Access Control（アクセス制御の不備）」の脆弱性をデモンストレーションするためのサンプルアプリケーションです。

## 脆弱性の概要

`MemoView`クラスでは、ユーザー認証や認可のチェックを行わずに、メモIDを直接指定してメモの内容を取得できます。これにより、他のユーザーのメモにも不正にアクセスできてしまいます。

```python
class MemoView(APIView):
    def get(self, request, memo_id):
        memo = Memo.objects.get(id=memo_id)  # 他人のメモにもアクセス可能
        serializer = MemoSerializer(memo)
        return Response(serializer.data)
```

## セットアップ

1. 仮想環境を作成・有効化
```bash
python3 -m venv venv
source venv/bin/activate
```

2. 依存関係をインストール
```bash
pip install -r requirements.txt
```

3. マイグレーション実行
```bash
python manage.py makemigrations
python manage.py migrate
```

4. サンプルデータ作成
```bash
python manage.py shell -c "
from django.contrib.auth.models import User
from memos.models import Memo

# ユーザー作成
user1 = User.objects.create_user(username='user1', password='password123er2 = User.objects.create_user(username='user2', password=password123 メモ作成
Memo.objects.create(title='サンプルメモ', content=これはuser1のサンプルです', owner=user1)
Memo.objects.create(title='user2密メモ', content='これはuser2の機密情報です。他のユーザーには見せられません。', owner=user2)
Memo.objects.create(title='user2業務メモ', content=明日の会議資料を準備する。重要な取引先の情報を含む。, owner=user2)```

5ー起動
```bash
python manage.py runserver
```

## 脆弱性のテスト

以下のURLにアクセスすると、認証なしで他人のメモが閲覧できます：

- `http://localhost:8000/api/memos/1/` - user1のメモ
- `http://localhost:8000/api/memos/2/` - user2の秘密メモ（本来はuser2のみアクセス可能であるべき）
- `http://localhost:8000/api/memos/3/` - user2の業務メモ（本来はuser2のみアクセス可能であるべき）

## 注意事項

このアプリケーションは教育・デモンストレーション目的のため、意図的にセキュリティ上の脆弱性を含んでいます。実際のプロダクション環境では使用しないでください。 