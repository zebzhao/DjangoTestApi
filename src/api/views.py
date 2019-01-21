from rest_framework import generics
from django.shortcuts import get_object_or_404

from .models import Property
from .serializers import PropertySerializer


class PropertyView(generics.ListCreateAPIView):
    """
    get:
    Return a list of all the existing properties.

    post:
    Create a new property instance.
    """
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    def perform_create(self, serializer):
        author = get_object_or_404(Property, id=self.request.data.get('id'))
        return serializer.save(author=author)


class SinglePropertyView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    Return a property instance by id.

    put:
    Update an entire property instance by id.

    patch:
    Partially update a property instance by id.

    delete:
    Delete a property instance by id.
    """
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
