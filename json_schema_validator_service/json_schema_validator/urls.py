# json_schema_validator/urls.py

from django.urls import path
from .views import ValidateJSONView

urlpatterns = [
    path('', ValidateJSONView.as_view(), name='validate_json'),
]