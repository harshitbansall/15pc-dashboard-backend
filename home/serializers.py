from rest_framework import serializers

from .models import *


class PaymentSerializer(serializers.ModelSerializer):
    timestamp = serializers.SerializerMethodField("get_timestamp")
    amount = serializers.SerializerMethodField("get_amount")

    class Meta:
        model = Payment
        fields = ('timestamp', 'amount')

    def get_amount(self, obj):
        return {"float": obj.amount, "string": f"₹ {obj.amount:,.2f}"}

    def get_timestamp(self, obj):
        return {"stamp": obj.created_at, "string": obj.created_at.strftime("%d %B %Y")}
