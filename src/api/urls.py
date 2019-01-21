from django.urls import path

from .views import PropertyView, SinglePropertyView


urlpatterns = [
    path('properties/', PropertyView.as_view()),
    path('properties/<int:pk>', SinglePropertyView.as_view()),
]
