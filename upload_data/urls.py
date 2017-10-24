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

from upload_data import views


urlpatterns = [
#     url(r'^admin/', admin.site.urls),
    
    url(r'^upload_good/', views.upload_good), 
    
    url(r'^search_upload_data/', views.search_upload_data), 
    url(r'^delete_upload_data/', views.del_upload_data),
    url(r'^edit_upload_data/', views.edit_upload_data),
    url(r'^show_upload_data/', views.show_upload_data),
    url(r'^show_wrong_data/', views.show_wrong_data),
    url(r'^show_personal_task/', views.show_personal_task),
    url(r'^upload_data/', views.upload_data),
    url(r'^show_tasks/', views.show_tasks),
    url(r'^get_tasks/', views.get_tasks),
    url(r'^get_task_area/', views.get_task_area),
    url(r'^get_task_city/', views.get_task_city),
    url(r'^get_task_province/', views.get_task_province),
    url(r'^gold_withdraw/', views.gold_withdraw),
    url(r'^intergral_withdraw/', views.intergral_withdraw),
    url(r'^bank_bind/', views.bank_bind),
    url(r'^complete_user_info/', views.complete_user_info),
    url(r'^show_personal_info/', views.show_personal_info),
    url(r'^show_base_info/', views.show_base_info),
    url(r'^register/', views.register),
    url(r'^send_msg/', views.send_msg),
    url(r'^login/', views.login),
    url(r'^logout/', views.logout),
]
