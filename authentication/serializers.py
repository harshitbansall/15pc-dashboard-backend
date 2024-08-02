from datetime import datetime, timedelta

from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(min_length=5, max_length=50, required=True)
    email = serializers.CharField(min_length=6, required=True)
    password = serializers.CharField(min_length=8, write_only=True, required=True)
    raw_password = serializers.CharField(min_length=8)

    class Meta:
        model = User
        fields = ('full_name', 'email', 'password', 'raw_password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        return user


class ConfigUserSerializer(serializers.ModelSerializer):
    # amount_invested = serializers.SerializerMethodField("get_amount_invested")
    # amount_invested_str = serializers.SerializerMethodField("get_amount_invested_str")
    # earned_interest = serializers.SerializerMethodField("get_earned_interest")
    # earned_interest_str = serializers.SerializerMethodField("get_earned_interest_str")


    class Meta:
        model = User
        fields = ('full_name', 'email', 'profile_img_url')
        # fields = ('full_name', 'email', 'profile_img_url','amount_invested', 'amount_invested_str', 'earned_interest', 'earned_interest_str')

    # def get_amount_invested(self, obj):
    #     self.payments_qs = obj.payment_set.all()
    #     self.amount_invested = round(sum([x.amount for x in self.payments_qs]), 2)
    #     return self.amount_invested

    # def get_amount_invested_str(self, obj):
    #     return f"₹ {self.amount_invested:,.2f}"

    # def get_earned_interest(self, obj):
    #     all_interests = []
    #     for payment in self.payments_qs:
    #         days_from_payment = (datetime.today() - payment.created_at.replace(tzinfo=None)).days
    #         interest_of_payment = (payment.amount * 0.00041 * days_from_payment)
    #         all_interests += [interest_of_payment]
    #     self.earned_interest = round(sum(all_interests), 2)
    #     return self.earned_interest
    
    # def get_earned_interest_str(self, obj):
    #     return f"₹ {self.earned_interest:,.2f}"