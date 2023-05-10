from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    roll_no = serializers.IntegerField()
    city = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Student.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        instance = old data stored in database
        validated_data = new data from user for updatation
        """
        instance.name = validated_data.get('name', instance.name)
        instance.roll_no = validated_data.get('roll_no', instance.roll_no)
        instance.city = validated_data.get('city', instance.city)
        instance.save()
        return instance

    def validate_name(self, value):
        """
        Charfield validation'
        used for single field
        """
        if len(value) > 5:
            raise serializers.ValidationError("Length is greater than 5")
        return value

    def validate(self, data):
        """
        object field validation
        used for multiple field
        """
        nm = data.get("name")
        ct = data.get("city")
        if nm != nm.lower() and ct != ct.lower():
            raise serializers.ValidationError("name and city must be in lower case")
        return data


