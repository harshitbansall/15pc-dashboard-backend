from django.urls import path

from .views import Dashboard, DashboardAccountValueGraph

urlpatterns = [
    path('dashboard', Dashboard.as_view(), name='Dashboard'),
    path('accountValueGraph', DashboardAccountValueGraph.as_view(), name='DashboardAccountValueGraph'),

]
