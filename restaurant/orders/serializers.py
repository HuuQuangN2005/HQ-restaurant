from rest_framework import serializers
from orders.models import Order, OrderDetail
from products.serializers import SimpleFoodSerializer
from users.serializers import AddressSerializer 

class OrderDetailSerializer(serializers.ModelSerializer):
    food_info = SimpleFoodSerializer(source="food", read_only=True)
    
    class Meta:
        model = OrderDetail
        fields = [
            "uuid", 
            "food",    
            "food_info",
            "quantity", 
            "unit_price", 
            "note"
        ]
        read_only_fields = ["uuid", "unit_price"]

class OrderSerializer(serializers.ModelSerializer):
    details = OrderDetailSerializer(many=True)
    address_info = AddressSerializer(source="address", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Order
        fields = [
            "uuid", 
            "customer", 
            "address", 
            "address_info",
            "status", 
            "status_display", 
            "total_price", 
            "is_paid", 
            "details", 
            "created_date"
        ]
        read_only_fields = ["uuid", "customer", "status", "total_price", "created_date"]

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        user = self.context['request'].user    
        order = Order.objects.create(customer=user, **validated_data)
        total = 0
        
        for detail in details_data:
            food_item = detail['food']
            qty = detail['quantity']
            current_price = food_item.price
            
            OrderDetail.objects.create(
                order=order,
                food=food_item,
                quantity=qty,
                unit_price=current_price,
                note=detail.get('note')
            )
            
            total += (current_price * qty)
        
        order.total_price = total
        order.save()
        
        return order