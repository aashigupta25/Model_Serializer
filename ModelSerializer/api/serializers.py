from attr import field
from rest_framework import serializers
from .models import Person

# Model Serializer
class PersonSerializer(serializers.ModelSerializer):
    # first_name = serializers.CharField(read_only = True)
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'age']
        read_only_fields = ['first_name', 'last_name']
        # extra_kwargs = {'name':{'read_only': True}}


