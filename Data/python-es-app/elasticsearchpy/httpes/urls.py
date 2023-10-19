from django.urls import path
from .views import CreateIndexView, InsertCustomDataView

app_name = "httpes"  # Namespace

urlpatterns = [
    path("create-index/", CreateIndexView.as_view(), name="create-index"),
    path("insert-data/", InsertCustomDataView.as_view(), name="insert-data"),
]
