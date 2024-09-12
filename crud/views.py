from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.apps import apps
from .serializers import get_dynamic_serializer

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def dynamic_model_view(request):
    model_type = request.GET.get('type')
    if not model_type:
        return Response({"error": "Model type is required."}, status=400)
    try:
        Model = apps.get_model('crud', model_type.capitalize())
    except LookupError:
        return Response({"error": "Invalid model type."}, status=400)
    DynamicSerializer = get_dynamic_serializer(Model)

    if request.method == 'GET':
        queryset = Model.objects.all()
        serializer = DynamicSerializer(queryset, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DynamicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    elif request.method == 'PUT':
        obj_id = request.data.get('id')
        instance = Model.objects.filter(id=obj_id).first()
        if not instance:
            return Response({"error": "Object not found"}, status=404)
        serializer = DynamicSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        obj_id = request.data.get('id')
        instance = Model.objects.filter(id=obj_id).first()
        if instance:
            instance.delete()
            return Response(status=204)
        return Response({"error": "Object not found"}, status=404)
