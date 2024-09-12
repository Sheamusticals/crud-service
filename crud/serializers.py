from rest_framework import serializers
from django.apps import apps

# Generate serializer dynamically based on the model class
def get_dynamic_serializer(model_class):
    """Create a serializer class dynamically for a given model."""
    class DynamicSerializer(serializers.ModelSerializer):
        class Meta:
            model = model_class
            fields = '__all__'  # Use all fields for simplicity, you can adjust this

    return DynamicSerializer
