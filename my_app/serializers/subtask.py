from rest_framework import serializers
from my_app.models import SubTask


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = [
            'id',
            'title',
            'description',
            'status',
            'owner',

        ]


class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(
        read_only=True
    )
    class Meta:
        model = SubTask
        fields = '__all__'
        # extra_kwargs = {
        #     "created_at": {
        #         "read_only": True
        #     }
        # }