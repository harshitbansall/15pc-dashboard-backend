import json
import time
from datetime import datetime, timedelta

from django.contrib.auth import authenticate, login
from django.shortcuts import HttpResponse, redirect, render
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PaymentSerializer


class Dashboard(APIView):
    def get(self, request):
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


class DashboardAccountValueGraph(APIView):
    def get(self, request):
        date_today = datetime.today().replace(
            tzinfo=None, hour=0, minute=0, second=0, microsecond=0)
        user_date_joined = request.user.date_joined.replace(
            tzinfo=None, hour=0, minute=0, second=0, microsecond=0)

        days_from_joined = (date_today - user_date_joined).days

        payments_qs = request.user.payment_set.all()

        if payments_qs.exists() == False:
            return Response(data={"success": "true","data": []}, status=status.HTTP_200_OK)

        all_payments = {}
        for payment in payments_qs:
            all_payments[payment.created_at.replace(tzinfo=None, hour=0, minute=0, second=0, microsecond=0)] = [j.amount for j in payments_qs if j.created_at.replace(
                tzinfo=None, hour=0, minute=0, second=0, microsecond=0) == payment.created_at.replace(tzinfo=None, hour=0, minute=0, second=0, microsecond=0)]

        return_data = []
        currentInvested = 0
        cuurentInterest = 0
        for x in range(days_from_joined):
            currentDate = (user_date_joined + timedelta(days=x))

            currentInvested += (currentInvested * 0.00041)

            if currentDate in all_payments.keys():
                currentInvested += sum(all_payments[currentDate])

            return_data += [
                {
                    "date": currentDate.strftime('%Y-%m-%d'),
                    "invested": round(currentInvested, 2),
                    "interest": round((currentInvested * 0.00041) * x,2)
                }
            ]

        data = {
            "success": "true",
            "data": return_data
        }
        return Response(data=data, status=status.HTTP_200_OK)
