import json
import time
from datetime import datetime

from django.contrib.auth import authenticate, login
from django.shortcuts import HttpResponse, redirect, render
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PaymentSerializer


class Dashboard(APIView):
    def get(self, request):
        # time.sleep(2)
        payments_qs = request.user.payment_set.all()
        amount_invested = round(sum([x.amount for x in payments_qs]), 2)

        all_interests = []
        all_daily_earnings = []
        for payment in payments_qs:
            days_from_payment = (datetime.today() -
                                 payment.created_at.replace(tzinfo=None)).days
            daily_earning = payment.amount * 0.00041
            interest_of_payment = (daily_earning * days_from_payment)
            all_interests += [interest_of_payment]
            all_daily_earnings += [daily_earning]
        earned_interest = round(sum(all_interests), 2)
        daily_earnings = round(sum(all_daily_earnings), 2)

        data = {
            "success": "true",
            # "full_name": request.user.full_name,
            # "email": request.user.email,
            "amount_invested": {"float": amount_invested, "string": f"₹ {amount_invested:,.2f}"},
            "earned_interest": {"float": earned_interest, "string": f"₹ {earned_interest:,.2f}"},
            "total_portfolio": {"float": (amount_invested + earned_interest), "string": f"₹ {(amount_invested + earned_interest):,.2f}"},
            "daily_earnings": {"float": daily_earnings, "string": f"₹ {daily_earnings:,.2f}"},
            "recent_fundings": PaymentSerializer(payments_qs[:5], many=True).data,
        }
        return Response(data=data, status=status.HTTP_200_OK)
