from rest_framework import serializers
from users.serializers import SimpleAccountSerializer
from actions.models import Comment

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