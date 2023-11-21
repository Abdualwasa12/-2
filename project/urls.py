"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('accounts/', include('accounts.urls',namespace='accounts')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('employee/',include('employee.urls',namespace='employee')),
    path('safe/',include('safe.urls',namespace='safe')),
    path('dealer/',include('dealer.urls',namespace='dealer')),
    path('transactions/',include('transactions.urls',namespace='transactions') ),
    path('invoice/',include('invoice.urls',namespace='invoice') ),
    path('material/',include('material.urls',namespace='material') ),
]