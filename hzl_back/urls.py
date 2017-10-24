"""hzl_data URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from hzl_back import views


urlpatterns = [
#     url(r'^admin/', admin.site.urls),
    url(r'^intergral_withdraw_opt/(\d*)/(\d*)', views.intergral_withdraw_opt),
    url(r'^intergral_withdraw_show/', views.intergral_withdraw_show),
    url(r'^merchant_info_opt/(\d*)/(\d*)/(.*)', views.merchant_info_opt),
    url(r'^merchant_info_show/', views.merchant_info_show),
    url(r'^release_tasks/', views.release_tasks),
    url(r'^superuser/', views.superuser),
    url(r'^get_task_province/', views.get_task_province),
    url(r'^get_task_city/', views.get_task_city),
    url(r'^get_task_area/', views.get_task_area),
    
]
