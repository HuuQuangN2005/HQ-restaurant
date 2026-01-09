from rest_framework import serializers
from users.serializers import SimpleAccountSerializer
from actions.models import Comment, Reservation

class CommentSerializer(serializers.ModelSerializer):
    
    def save(self, **kwargs):
        
        
        return super().save(**kwargs)
    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['account'] = SimpleAccountSerializer(instance.account).data
        
        return data

    class Meta:
        model = Comment
        fields = ['uuid', 'content', 'created_date', 'account', 'food']
        extra_kwargs = {
            'food': {
                'write_only': "True"
            }
        }
        
class SimpleReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["uuid","date", "status"]
        read_only_fields = ["uuid"]
        
class ReservationSerializer(SimpleReservationSerializer):
    account = SimpleAccountSerializer(read_only=True)
    status_label = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = SimpleReservationSerializer.Meta.model
        fields = SimpleReservationSerializer.Meta.fields + [
            "account", 
            "participants", 
            "notes", 
            "status_label"
        ]
        read_only_fields = ["uuid", "account", "status"]