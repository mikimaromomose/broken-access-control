from django.urls import path
from .views import MemoView

urlpatterns = [
    path('<int:memo_id>/', MemoView.as_view(), name='memo-detail'),
] 