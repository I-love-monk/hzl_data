import datetime
import json

from django.core import serializers
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt

from upload_data import models


# Create your views here.
def checksuperuser(main_fun):
    def _outer(request,*args,**kargs):
        if not request.session.get("current_superuser_id"):
            return JsonResponse({"status":500,"msg":"登录超时，请重新登录"})
        return main_fun(request,*args,**kargs)
    return _outer



@csrf_exempt
def superuser(request):
#     print(settings.BASE_DIR)
#     super_index = os.path.join(settings.BASE_DIR,"hzl_back\dist\index.html")
#     print(super_index)
    ret = {"msg":"","status":500}     
    if request.method == "POST":
        mobile = request.POST.get("username")
        password = request.POST.get("pwd")
        print(mobile,password)
        user = models.Superuser.objects.filter(mobile=mobile,password=password)
        if user:
            request.session["current_superuser_id"] = user[0].id
            ret["status"] = 200
        else:
            ret["msg"]="用户名或密码错误" 
        return JsonResponse(ret)
    return render_to_response(r"G:\Eclipse\hzl_data\hzl_back\templates\index.html")




#后台操作
@checksuperuser
def release_tasks(request):
    ret = {"status":200,"msg":"",}
    
    if request.method == "POST":
        province = request.POST.get("province")
        city = request.POST.get("city")
        area = request.POST.get("area")
        detail_address =request.POST.get("detail_address")
        amount = request.POST.get("amount")
        
        address = province+"-"+city+"-"+area+"-"+detail_address
        models.Tasks.objects.create(address=address,total_task_num=amount,opt_time=datetime.datetime.now().strftime("%Y-%m-%d"))
    obj_data = models.Tasks.objects.all()
    obj_data = json.loads(serializers.serialize("json", obj_data))
    ret["list"] = obj_data    
    return JsonResponse(ret)


@checksuperuser
def merchant_info_show(request):
    ret = {"status":200,"msg":"",}
    try:
        merchant_info_list = models.Merchant_info.objects.filter(status=0) 
        merchant_info_list = json.loads(serializers.serialize("json", merchant_info_list))
        ret["list"] = merchant_info_list
    except Exception as e:
        ret = {"status":500,"msg":e,}
    return JsonResponse(ret)


@checksuperuser
def merchant_info_opt(request,opt_type,content_id,remark):
    ret = {"status":200,"msg":"",}
    if int(opt_type) == 1:
        models.Merchant_info.objects.filter(id=content_id).update(status=1)
    elif int(opt_type) == 2:
        models.Merchant_info.objects.filter(id=content_id).update(status=-1,remark=remark)
    
    return JsonResponse(ret)


@checksuperuser
def intergral_withdraw_show(request):
    ret = {"status":200,"msg":"",}
    try:
        intergral_withdraw_list = models.Withdraw_record.objects.filter(status=0,opt_type=1,) 
        intergral_withdraw_list = json.loads(serializers.serialize("json", intergral_withdraw_list))
        ret["list"] = intergral_withdraw_list
    except Exception as e:
        ret = {"status":500,"msg":e,}
    return JsonResponse(ret)


@checksuperuser
def intergral_withdraw_opt(request,opt_type,content_id):
    ret = {"status":200,"msg":"",}
    if int(opt_type) == 1:
        models.Withdraw_record.objects.filter(id=content_id).update(status=1)
    elif int(opt_type) == 2:
        models.Withdraw_record.objects.filter(id=content_id).update(status=-1)
    
    return JsonResponse(ret)


def get_task_province(request):
    ret = {"msg":"","status":200}
    try:
        province_list = set()
        province_data = models.Area_code.objects.all()
        for i in province_data:
            province_list.add(i.province)
        ret["province_list"] = list(province_list)
        print(province_list)
    except Exception as e:
        ret = {"msg":e,"status":500}
    return JsonResponse(ret)
    
def get_task_city(request):
    ret = {"msg":"","status":200}
    if request.method == "POST":
        try:
            province = request.POST.get("province")
            if not province:
                province = "广东省"
            data = models.Area_code.objects.filter(province=province)
            cities_list = json.loads(serializers.serialize("json", data))
            ret["cities_list"] = cities_list
        except Exception as e:
            ret = {"msg":e,"status":500}
    return HttpResponse(json.dumps(ret))

def get_task_area(request):
    ret = {"msg":"","status":200}
    if request.method == "POST":
        try:
            city_name = request.POST.get("city")
            if city_name[:2] in ["台湾","香港","澳门"]:
                city_id = models.Areas.objects.filter(shortname=city_name[:2])[0].id
            else:
                city_id = models.Areas.objects.filter(areaname=city_name)[0].id
            data = models.Areas.objects.filter(parentid=city_id)
            areas_list = json.loads(serializers.serialize("json", data))
            ret["areas_list"] = areas_list
        except Exception as e:
            ret = {"msg":e,"status":500}
    return HttpResponse(json.dumps(ret))

