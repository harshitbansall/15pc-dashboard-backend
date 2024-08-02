from django.db import models

from authentication.models import User


class Payment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)

    class Meta:
        db_table = 'payments'

    def __str__(self):
        return f'{self.user} : {self.amount}'

# class Balance(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     amount = models.FloatField(default=0)

#     class Meta:
#         db_table = 'balances'

#     def __str__(self):
#         return '{}'.format(self.user)