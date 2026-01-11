from rest_framework import serializers
from django.db import transaction
from users.serializers import SimpleAccountSerializer, AddressSerializer
from actions.models import Comment, Reservation, Order, OrderDetail
from products.serializers import SimpleFoodSerializer
from users.models import Address
from products.models import Food


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ["uuid", "content", "created_date", "account", "food"]
        write_only_fields = ["food"]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["account"] = SimpleAccountSerializer(instance.account).data

        return data


class SimpleReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["uuid", "date", "status"]
        read_only_fields = ["uuid"]


class ReservationSerializer(SimpleReservationSerializer):
    account = SimpleAccountSerializer(read_only=True)
    status_label = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = SimpleReservationSerializer.Meta.model
        fields = SimpleReservationSerializer.Meta.fields + [
            "account",
            "participants",
            "notes",
            "status_label",
        ]
        read_only_fields = ["uuid", "account", "status"]


class OrderDetailSerializer(serializers.ModelSerializer):

    food = serializers.SlugRelatedField(slug_field="uuid", queryset=Food.objects.all())

    class Meta:
        model = OrderDetail
        fields = ["uuid", "food", "quantity", "price", "note"]
        read_only_fields = ["uuid", "price"]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if instance.food:
            data["food"] = SimpleFoodSerializer(instance.food).data
        return data


class SimpleOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["uuid", "status", "is_paid", "created_date"]
        read_only_fields = ["uuid", "status", "created_date"]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if instance.status:
            data["status"] = instance.get_status_display()
        return data


class OrderSerializer(SimpleOrderSerializer):
    details = OrderDetailSerializer(many=True)
    address = serializers.SlugRelatedField(
        slug_field="uuid",
        queryset=Address.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta(SimpleOrderSerializer.Meta):
        fields = SimpleOrderSerializer.Meta.fields + [
            "account",
            "address",
            "total_price",
            "details",
        ]
        read_only_fields = SimpleOrderSerializer.Meta.read_only_fields + [
            "account",
            "total_price",
        ]

    def create(self, validated_data):
        details_data = validated_data.pop("details")

        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            total = 0

            for detail in details_data:
                food = detail["food"]
                quantity = detail["quantity"]
                current_price = food.price

                OrderDetail.objects.create(
                    order=order,
                    food=food,
                    quantity=quantity,
                    price=current_price,
                    note=detail.get("note"),
                )
                total += current_price * quantity

            order.total_price = total
            order.save()

        return order

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if instance.account:
            data["account"] = SimpleAccountSerializer(instance.account).data

        if instance.address:
            data["address"] = AddressSerializer(instance.address).data
        
        if instance.details:
            data["details"] = OrderDetailSerializer(instance.details.all(), many=True).data

        return data
