import _md5
import base64
import datetime
import json
import os

from django.contrib.sessions.models import Session
from django.core import serializers
from django.db.models.query_utils import Q
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, render_to_response
from django.views.decorators.csrf import csrf_exempt
import requests

from hzl_data import settings
from upload_data import models


# Create your views here.
# def checklogin(session_key):
#     pass
#     if Session.objects.filter(session_key=session_key):
#         
#         user_dict = Session.objects.get(session_key=session_key).get_decoded()
#     else:
#         user_dict = ""
#     return user_dict
def checklogin(main_fun):
    def _outer(request,*args,**kargs):
        if not request.session.get("current_user_id"):
#             return redirect("/api/login")
            return JsonResponse({"status":500,"msg":"登录超时，请重新登录"})
        return main_fun(request,*args,**kargs)
    return _outer

class CJenoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj,datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj,datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self,obj)

def md5_password(password):
    m = _md5.md5()
    m.update(password.encode())
    temp = m.hexdigest()
    www=[]
    for i in range(len(temp)):
        aaa = chr(int(ord(str(temp[i]))) ^ int(ord("s")))
        www.append(aaa)
    return "".join(www)


@csrf_exempt
def login(request):
    ret = {"msg":"","status":500}     
    if request.method == "POST":
        mobile = request.POST.get("username")
        password = request.POST.get("pwd")
#         print(mobile,password)
        pwd = md5_password(password)
        user = models.Register_user.objects.filter(mobile=mobile,password=password)
        if user:
            if user[0].status<0:
                ret["msg"]="账号异常，请联系客服"
                return JsonResponse(ret)
            request.session["current_user_id"] = user[0].id
            ret["status"] = 200
            if not models.CoinInfo.objects.filter(user_id=user[0].id):
                models.CoinInfo.objects.create(user_id=user[0].id)
            if not models.UserInfo.objects.filter(user_id=user[0].id): 
                models.UserInfo.objects.create(user_id=user[0].id)
            if not models.BankBind.objects.filter(user_id=user[0].id): 
                models.BankBind.objects.create(user_id=user[0].id,bank_id=0)
        else:
            user_temp = models.User.objects.using("search").filter(mobile=mobile,password=pwd)
            if user_temp:
#                 account = models.UserAccount.objects.using("search").filter(user_id=user_temp[0].id)[0]
                user = models.Register_user.objects.create(mobile=mobile,
                                                           password=password,
                                                           status=1,
                                                           user_name="",
                                                           pay_password="")
                request.session["current_user_id"] = user.id
                ret["status"] = 200
                if not models.CoinInfo.objects.filter(user_id=user.id):
                    models.CoinInfo.objects.create(user_id=user.id)
                if not models.UserInfo.objects.filter(user_id=user.id): 
                    models.UserInfo.objects.create(user_id=user.id)
                if not models.BankBind.objects.filter(user_id=user.id): 
                    models.BankBind.objects.create(user_id=user.id,bank_id=0)
            else:
                ret["msg"]="用户名或密码错误" 
        print(ret)
        return JsonResponse(ret)


@checklogin
def logout(request):
    ret = {"msg":"","status":200}
    try:
        del request.session["current_user_id"]
    except Exception as e:
        ret = {"msg":e,"status":500}
    return JsonResponse(ret)


#type=1 注册 2 提现 3绑定银行卡
def send_msg(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
#         body = json.loads(body_unicode)
        mobile = request.POST.get("mobile")
        imageCode = request.POST.get("imageCode")
        type = request.POST.get("type")
        ret={"status":200}
        parameters = {"action":"smsService.zbbSend","jsonString":""} 
         
        url = "http://hzl-api.jufeng.co/api"
        appid = "1493037951465"
        appsecret = "aa5009503ead3a60180779f1d1db3227"
        token = appid+appsecret
        m = _md5.md5()
        m.update(token.encode())
        token = m.hexdigest()
        temp = {"mobile":mobile,"type":type,"token":token,"tokenUserId":1,"imageCode":imageCode}
        temp = json.dumps(temp).encode(encoding='utf_8')
        temp =base64.b64encode(temp)
        parameters["jsonString"] = temp
        req = requests.post(url,parameters)
        resp = json.loads(req.text)
        print(resp)
        if resp["isSuccess"]:
            print(resp["data"])
            request.session["check_num"] = {str(type):{mobile:resp["data"]}}
#             print(request.session["check_num"])
        else:
            ret["status"] = 500
        ret["msg"] = resp["description"]
        print(ret["msg"])
        return HttpResponse(json.dumps(ret))
    return render_to_response("signup.html",ret)

@csrf_exempt    
def register(request):
    ret = {"msg":"","status":500}
    if request.method=="POST":
        
#         body_unicode = request.body.decode('utf-8')
#         print(body_unicode)
        mobile = request.POST.get("mobile")
        user_name = request.POST.get("username")
        if models.Register_user.objects.filter(mobile=mobile):
            ret["msg"] = "该用户已注册"
            return HttpResponse(json.dumps(ret))
        check_msg = request.POST.get("check_code")
        password = request.POST.get("pwd")
#         print(user_name,check_msg,password)
        if not (mobile and check_msg and password):
            ret["msg"] = "不能为空"
            return HttpResponse(json.dumps(ret))
        if request.session.get("check_num",False):
            if check_msg == request.session.get("check_num")['1'][mobile]:
                user = models.Register_user.objects.create(mobile=mobile,password=password,user_name=user_name)
                models.CoinInfo.objects.create(user_id=user.id)
                ret["status"]=200
                del request.session["check_num"]
            else:
                ret["msg"] = "验证码错误"
        else:
            ret["msg"] = "验证码异常"    
        return HttpResponse(json.dumps(ret)) 


@checklogin
def show_base_info(request):
    ret = {"status":200,"msg":""}
    try:
        user_id = request.session.get("current_user_id")
        
        mobile = models.Register_user.objects.filter(id=user_id)[0].mobile
        user_coin_info = models.CoinInfo.objects.filter(user_id=user_id)[0]
        hzl_user = models.User.objects.using("search").filter(mobile=mobile)
        if hzl_user:
            hzl_account = models.UserAccount.objects.using("search").filter(user_id=hzl_user[0].id)[0]
            hzl_level = models.UserLevel.objects.using("search").filter(user_id=hzl_user[0].id)[0].level
            avaliable_intergral = models.FlmAccount.objects.using("flm").filter(user_id=hzl_user[0].id)
            level = models.UserLevelConfig.objects.using("search").filter(level=hzl_level)[0].name
            
            account = hzl_user[0].account
            real_name = hzl_account.real_name
            id_card = hzl_account.id_card
            create_time = hzl_account.create_time.strftime("%Y-%m-%d")
        else:
            account = ""
            real_name = ""
            id_card = ""
            create_time = ""
        
        if avaliable_intergral:
            available_integral = avaliable_intergral[0].available_integral
        else:
            available_integral = 0
        bank_account = models.BankBind.objects.filter(user_id=user_id)
        if bank_account:
            bank_account = bank_account[0].bank_account
        else:
            bank_account=""
        info_msg = {}
        info_msg["level"] = level
        info_msg["account"] = account
        info_msg["mobile"] = mobile
        info_msg["real_name"] = real_name
        info_msg["id_card"] = id_card
        info_msg["create_time"] = create_time
        info_msg["avaliable_intergral"] = available_integral
        info_msg["intergral_num"] = user_coin_info.intergral_num
        info_msg["gold_num"] = user_coin_info.gold_num 
        info_msg["bank_account"] = bank_account
        ret["info_msg"] = info_msg
    except Exception as e:
        ret = {"status":500,"msg":e}
    
    return HttpResponse(json.dumps(ret))

@checklogin
def show_personal_info(request):
    ret = {"msg":"","status":200}
    try:
        user_id = request.session.get("current_user_id")
        mobile = models.Register_user.objects.filter(id=user_id)[0].mobile
        hzl_user = models.User.objects.using("search").filter(mobile=mobile)[0]
        hzl_account = models.UserAccount.objects.using("search").filter(user_id=hzl_user.id)[0]
        user_info = models.UserInfo.objects.filter(user_id=user_id)[0]
        hzl_level = models.UserLevel.objects.using("search").filter(user_id=hzl_user.id)[0].level
        level = models.UserLevelConfig.objects.using("search").filter(level=hzl_level)[0].name
        user_coin_info = models.CoinInfo.objects.filter(user_id=user_id)[0]
        info_msg = {}
        info_msg["level"] = level
        
        info_msg["account"] = hzl_user.account
        info_msg["mobile"] = mobile
        info_msg["real_name"] = hzl_account.real_name
        info_msg["id_card"] = hzl_account.id_card
        info_msg["create_time"] = hzl_account.create_time
        info_msg["intergral_num"] = user_coin_info.intergral_num
        info_msg["gold_num"] = user_coin_info.gold_num
        
        info_msg["job"] = user_info.job
        info_msg["hobby"] = user_info.hobby
        info_msg["qq"] = user_info.qq
        info_msg["wechat"] = user_info.wechat
        info_msg["email"] = user_info.email
        info_msg["emergency_contact_name"] = user_info.emergency_contact_name
        info_msg["emergency_contact_relation"] = user_info.emergency_contact_relation
        info_msg["emergency_contact_mobile"] = user_info.emergency_contact_mobile
        
        ret["info_msg"] = info_msg
    except Exception as e:
        ret["status"] = 500
        ret["msg"] = e
    return JsonResponse(ret)

@checklogin
def complete_user_info(request):
    ret = {"msg":"","status":200}
    user_id = request.session.get("current_user_id")
    if request.method == "POST":
        try:
            job = request.POST.get("job")
            hobby = request.POST.get("hobby")
            qq = request.POST.get("qq")
            wechat = request.POST.get("wechat")
            email = request.POST.get("email")
            emergency_contact_name = request.POST.get("emergency_contact_name")
            emergency_contact_relation = request.POST.get("emergency_contact_relation")
            emergency_contact_mobile = request.POST.get("emergency_contact_mobile")
            models.UserInfo.objects.filter(user_id=user_id).update(
                job=job,hobby=hobby,qq=qq,wechat=wechat,email=email,
                emergency_contact_name=emergency_contact_name,
                emergency_contact_relation=emergency_contact_relation,
                emergency_contact_mobile=emergency_contact_mobile
                )
        except Exception as e:
            ret["status"] = 500
            ret["msg"] = e
    return JsonResponse(ret)


@checklogin
def bank_bind(request):
    ret = {"msg":"","status":200}
    user_id = request.session.get("current_user_id")
    bank_list = models.BankList.objects.all()
    bank_list = json.loads(serializers.serialize("json", bank_list))
    
    if request.method == "POST":
        try:
            bank_id = request.POST.get("bank_id")
            real_name = request.POST.get("real_name")
            bank_account = request.POST.get("bank_account")
            bank_name = request.POST.get("bank_name")
            id_card = request.POST.get("id_card")
            pay_password = request.POST.get("pay_password")
            bank_mobile = request.POST.get("bank_mobile")
            check_msg = request.POST.get("check_msg")
            if request.session.get("check_num",False):
                if check_msg == request.session.get("check_num")['4'][bank_mobile]:
                    models.Register_user.objects.filter(id=user_id).update(pay_password=pay_password)
                    models.BankBind.objects.filter(user_id=user_id).update(bank_id=bank_id,
                                                                   real_name=real_name,
                                                                   bank_account=bank_account,
                                                                   bank_name=bank_name,
                                                                   id_card=id_card,
                                                                   bank_mobile=bank_mobile,
                                                                   )
                    ret["status"]=200
                    del request.session["check_num"]
                else:
                    ret["status"]=500
                    ret["msg"] = "验证码错误"
            else:
                ret["status"]=500
                ret["msg"] = "验证码异常" 
#             pay_pwd = md5_password(pay_password)
            
        except Exception as e:
            ret["status"] = 500
            ret["msg"] = e
        return JsonResponse(ret)
    ret["bank_list"] = bank_list
    return HttpResponse(json.dumps(ret))

#======================no check
@checklogin
def intergral_withdraw(request):
    user_id = request.session.get("current_user_id")
    bank_mobile = models.BankBind.objects.filter(user_id=user_id)[0].bank_mobile
    user_pay_password = models.Register_user.objects.filter(id=user_id)[0].pay_password
    bank_info = models.BankBind.objects.filter(user_id=user_id)[0]
    ret = {"status":200,"msg":""}
#     ret["type"] = "可用积分提现"
    ret["bank_account"] = bank_info.bank_account
    ret["bank_name"] = bank_info.bank_name
    try:
        if request.method=="POST":
            pay_password = request.POST.get("pay_password")
            mobile = request.POST.get("mobile")
            check_msg = request.POST.get("check_msg")
            amount_temp = request.POST.get("amount")
            task_id = request.POST.get("task_id")
            if not task_id:
                ret["status"] = 500
                ret["msg"] = "提现操作异常"
                return JsonResponse(ret)
            amount = models.solve_task_user.objects.filter(tasks_id=task_id)[0].solve_task_num
            if amount_temp != amount:
                ret["status"] = 500
                ret["msg"] = "提现操作异常"
                return JsonResponse(ret)
            if bank_mobile == mobile:
                if pay_password == user_pay_password:
                    if request.session.get("check_num",False):
                        if check_msg == request.session["check_num"]["2"][mobile]:
                            #
                            intergral_num = models.CoinInfo.objects.filter(user_id=user_id)[0].intergral_num
                            if int(amount)>int(intergral_num):
                                ret["status"] = 500
                                ret["msg"] = "提现金额超出"
                            else:
                                opt_record = mobile+"申请积分提现"+intergral_num
                                models.Withdraw_record.objects.create(user_id=user_id,opt_type=1,opt_record=opt_record,balance=int(intergral_num)-int(amount))
                                ret["msg"] = "操作成功"
                                ret["status"] = 200
                                del request.session["check_num"]
                        else:
                            ret["status"] = 500
                            ret["msg"] = "验证码错误"
                    else:
                        ret["status"] = 500
                        ret["msg"] = "验证码异常"
                else:
                    ret["status"] = 500
                    ret["msg"] = "支付密码错误"
            else:
                ret["status"] = 500
                ret["msg"] = "电话号码异常"
    except Exception as e:
        ret["status"] = 500
        ret["msg"] = e
    return JsonResponse(ret)
#     else:
#         return redirect("/intergral_withdraw")
    
#======================no check 
@checklogin    
def gold_withdraw(request):
    ret = {"msg":"","status":200}
    user_id = request.session.get("current_user_id")
    user_mobile = models.Register_user.objects.filter(id=user_id)[0].mobile
    user_pay_password = models.Register_user.objects.filter(id=user_id)[0].pay_password
    bank_info = models.BankBind.objects.filter(user_id=user_id)[0]
#     ret["type"] = "金币提现"
    if not bank_info.bank_account:
        ret["status"] = 500
        ret["msg"] = "银行卡未绑定"
        return JsonResponse(ret)
    ret["bank_account"] = bank_info.bank_account
    ret["bank_name"] = bank_info.bank_name
    
    
    if request.method=="POST":
        pay_password = request.POST.get("pay_password")
        mobile = request.POST.get("mobile")
        check_msg = request.POST.get("check_msg")
        amount = request.POST.get("amount")
        if user_mobile == mobile:
            if pay_password == user_pay_password:
                if request.session.get("check_num",False):
                    if check_msg == request.session["check_num"]["3"][mobile]:
                        #
                        gold_num = models.CoinInfo.objects.filter(user_id=user_id)[0].gold_num
                        if int(amount)>int(gold_num):
                            ret["msg"] = "提现金额超出"
                        else:
                            opt_record = mobile+"申请金币提现"+gold_num
                            models.Withdraw_record.objects.create(user_id=user_id,opt_type=2,opt_record=opt_record,balance=int(gold_num)-int(amount))
                            ret["msg"] = "操作成功"
                            ret["status"] = 200
                            del request.session["check_num"]
                    else:
                        ret["msg"] = "验证码错误"
                else:
                    ret["msg"] = "验证码异常"
            else:
                ret["msg"] = "支付密码错误"
        else:
            ret["msg"] = "电话号码异常"
    return JsonResponse(ret)
#     else:
#         return redirect("/intergral_withdraw")
  
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


def show_tasks_by_time(request):
    ret = {"status":200,"msg":""}
    if request.method == "POST":
        try:
            tasks_time = request.POST.get("tasks_time")
            if not tasks_time:
                tasks_time = datetime.datetime.now().strftime("%Y-%m-%d")
            tasks_obj = models.Tasks.objects.filter(status=0,opt_time=tasks_time)
            obj_list = json.loads(serializers.serialize("json", tasks_obj))
            ret["list"] = obj_list
        except Exception as e:
            ret = {"status":500,"msg":e}
    return HttpResponse(json.dumps(ret))


def show_tasks(request):
    ret = {"status":200,"msg":""}
    if request.method == "POST":
        try:
            province = request.POST.get("province")
            if not province:
                province = "广东省"
            tasks_obj = models.Tasks.objects.filter(status=0,address__contains=province)
            obj_list = json.loads(serializers.serialize("json", tasks_obj))
            ret["list"] = obj_list
        except Exception as e:
            ret = {"status":500,"msg":e}
    return HttpResponse(json.dumps(ret))

@checklogin  
def show_personal_task(request):
    #显示个人任务情况
    ret = {"status":200,"msg":""}
    personal_task_list = []
    user_id = request.session.get("current_user_id")
    if request.method == "POST":
        try:
            province = request.POST.get("province")
            if not province:
                province = "广东省"
            personal_task = models.solve_task_user.objects.filter(solve_user_id=user_id,province=province)
            for i in personal_task:
                address = models.Tasks.objects.filter(id=i.tasks_id)[0].address
                check_task_num = models.Merchant_info.objects.filter(address__contains=address,status=1).count()
                dict_info = {
                    "address":address,
                    "total_task_num":models.Tasks.objects.filter(id=i.tasks_id)[0].total_task_num,
                    "get_task_num":i.get_task_num,
                    "solve_task_num":check_task_num,
                    "task_id":i.tasks_id,
                    }
                personal_task_list.append(dict_info)
            ret["personal_task"] = personal_task_list
        except Exception as e:
            ret = {"status":500,"msg":e}
    return HttpResponse(json.dumps(ret))

@checklogin   
def get_tasks(request):
    user_id = request.session.get("current_user_id")
    ret = {"status":200,"msg":""}
    if request.method == "POST":
        amount = request.POST.get("amount")
        task_id =request.POST.get("task_id")
        province = request.POST.get("province")
        
        if not amount:
            ret["status"] = 500
            ret["msg"] = "数量异常"
            return HttpResponse(json.dumps(ret))
        if not models.solve_task_user.objects.filter(tasks_id=task_id,solve_user_id=user_id):
            if int(amount)%100 == 0:
                if models.Tasks.objects.filter(id=task_id):
                    models.solve_task_user.objects.create(solve_user_id=user_id,get_task_num=amount,
                                                          tasks_id=task_id,province=province)
                    total_task_num = models.Tasks.objects.filter(id=task_id)[0].total_task_num
                    models.Tasks.objects.filter(id=task_id).update(avali_task_num=int(total_task_num)-int(amount))
                else:
                    ret["status"] = 500
                    ret["msg"] = "任务异常"
            else:
                ret["status"] = 500
                ret["msg"] = "数量异常"
        else:
            ret["status"] = 500
            ret["msg"] = "该任务已领取"
    return HttpResponse(json.dumps(ret))


@checklogin   
def upload_data(request):
    ret = {"status":200,"msg":"",}
    user_id = request.session.get("current_user_id")
    if request.method == "POST":
        address = request.POST.get("address")
        industry = request.POST.get("industry")
        mobile = request.POST.get("mobile")
        name = request.POST.get("name")
        feature = request.POST.get("feature")
        pic_file = request.POST.get("pic_file")
        print(address,industry,mobile,name,feature,pic_file)
        print(1)
        if models.Merchant_info.objects.filter(mobile=mobile,industry=industry):
            models.Merchant_info.objects.create(address=address,mobile=mobile,name=name,
                                                feature=feature,pic_file=pic_file,industry=industry,
                                                upload_user_id=user_id,status=-1,remark="重复上传")
            ret["status"] = 500
            ret["msg"] = "重复上传"
        else:
            print(1)
            models.Merchant_info.objects.create(address=address,mobile=mobile,name=name,
                                                feature=feature,pic_file=pic_file,industry=industry,
                                                upload_user_id=user_id)
            
            for tk in models.Tasks.objects.all():
                print(tk.address)
                if tk.address in address.replace(",","-"):
                    task_id = tk.id
                    break
                else:
                    task_id = ""
            print(task_id)
            if task_id:
                solve_num = models.solve_task_user.objects.filter(solve_user_id=user_id,tasks_id=task_id)
                if solve_num:
                    solve_num = solve_num[0].solve_task_num
                    models.solve_task_user.objects.filter(solve_user_id=user_id,tasks_id=task_id).update(solve_task_num=solve_num+1)
                else:
                    ret["status"] = 500
                    ret["msg"] = "上传地址与所接任务地址不符"
            else:
                ret["status"] = 500
                ret["msg"] = "上传地址不在任务列表内"
        
    return JsonResponse(ret)

@checklogin
def show_wrong_data(request):
    ret = {"status":200,"msg":"",}
    try:
        user_id = request.session.get("current_user_id")
        repitition_data = models.Merchant_info.objects.filter(upload_user_id=user_id,status=-1)
        repitition_data = json.loads(serializers.serialize("json", repitition_data))
        ret["list"] = repitition_data
    except Exception as e:
        ret = {"status":500,"msg":e,}
    return HttpResponse(json.dumps(ret))

@checklogin
def show_upload_data(request):
    ret = {"status":200,"msg":"",}
    try:
        user_id = request.session.get("current_user_id")
        upload_data_info = models.Merchant_info.objects.filter(upload_user_id=user_id,status=0)
        upload_data_info = json.loads(serializers.serialize("json", upload_data_info))
        ret["list"] = upload_data_info
    except Exception as e:
        ret = {"status":500,"msg":e,}
    return HttpResponse(json.dumps(ret))



@checklogin
def edit_upload_data(request):
    ret = {"status":200,"msg":"",}
    try:
            
        content_id = request.GET.get("content_id")
        user_id = request.session.get("current_user_id")
        info = models.Merchant_info.objects.filter(id=content_id)
        info = json.loads(serializers.serialize("json", info))
        ret["list"] = info
        if request.method == "POST":
            content_id = request.POST.get("content_id")
            address = request.POST.get("address")
            industry = request.POST.get("industry")
            mobile = request.POST.get("mobile")
            name = request.POST.get("name")
            feature = request.POST.get("feature")
            pic_file = request.POST.get("pic_file")
            if models.Merchant_info.objects.filter(mobile=mobile,industry=industry):
                models.Merchant_info.objects.filter(id=content_id).update(address=address,mobile=mobile,name=name,
                                                    feature=feature,pic_file=pic_file,industry=industry,
                                                    upload_user_id=user_id,status=-1)
                ret["status"] = 500
                ret["msg"] = "重复更新"
            else:
                models.Merchant_info.objects.filter(id=content_id).update(address=address,mobile=mobile,name=name,
                                                    feature=feature,pic_file=pic_file,industry=industry,
                                                    upload_user_id=user_id,status=0)
            ret["list"] = ""
    except Exception as e:
        ret = {"status":500,"msg":e,}
    
    return JsonResponse(ret)



@checklogin
def del_upload_data(request):
    ret = {"status":200,"msg":"",}
    try:
        if request.method == "POST":
            content_id = request.POST.get("content_id")
            user_id = request.session.get("current_user_id")
            temp = models.Merchant_info.objects.filter(id=content_id,upload_user_id=user_id)
            if temp:
                temp.delete()
            else:
                ret["msg"] = "无权删除"
    except Exception as e:
        ret = {"status":500,"msg":e,}
    return JsonResponse(ret)

@checklogin
def search_upload_data(request):
    ret = {"status":200,"msg":"",}
    try:
        user_id = request.session.get("current_user_id")
        if request.method == "POST":
            content = request.POST.get("content")
            list_temp = models.Merchant_info.objects.filter(Q(upload_user_id=user_id),
                                                Q(mobile__contains=content)|Q(industry__contains=content)|Q(feature__contains=content)|Q(name__contains=content))
            
            ret["list"] = json.loads(serializers.serialize("json", list_temp))
    except Exception as e:
        ret = {"status":500,"msg":e,}
    
    return JsonResponse(ret)


@checklogin
def upload_good(request):
    ret = {"status":200,"msg":"",}
    user_id = request.session.get("current_user_id")
    
    index = request.GET.get("index")
    if not index:
        index = 0
    begin = int(index)*10
    end = begin+10
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        introduction = request.POST.get("introduction")
        pic_file = request.POST.get("pic_file")
        if models.Goods_list.objects.filter(name=name):
            ret["status"] = 500
            ret["msg"] = "重复上传"
        else:
            models.Goods_list.objects.create(name=name,
                                             price=price,
                                             pic_file=pic_file,
                                             introduction=introduction,
                                             upload_user_id=user_id)
        return JsonResponse(ret)
    total = models.Goods_list.objects.all().count()
    obj_list = models.Goods_list.objects.filter(status=0).order_by("id")[begin:end]
    ret["list"] = json.loads(serializers.serialize("json", obj_list))
    ret["total"] = total
    return JsonResponse(ret)











