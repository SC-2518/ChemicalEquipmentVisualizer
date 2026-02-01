from rest_framework import serializers
from .models import Dataset, Equipment

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['id', 'equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature']

class DatasetSerializer(serializers.ModelSerializer):
    # Retrieve equipment details for detail view
    equipment = EquipmentSerializer(many=True, read_only=True)

    class Meta:
        model = Dataset
        fields = ['id', 'filename', 'upload_date', 'total_records', 'avg_flowrate', 'avg_pressure', 'avg_temperature', 'equipment']
        read_only_fields = ['id', 'upload_date', 'total_records', 'avg_flowrate', 'avg_pressure', 'avg_temperature', 'equipment']

class DatasetListSerializer(serializers.ModelSerializer):
    # Simplified serializer for list view (no equipment details)
    class Meta:
        model = Dataset
        fields = ['id', 'filename', 'upload_date', 'total_records', 'avg_flowrate', 'avg_pressure', 'avg_temperature']

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
