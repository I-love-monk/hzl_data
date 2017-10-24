from django.db import models

# Create your models here.

class Goods_list(models.Model):
    name = models.CharField(max_length=250)
    price = models.CharField(max_length=50)
    introduction = models.TextField() 
    upload_user_id = models.CharField(max_length=50) 
    upload_time = models.DateField(auto_now_add=True)
    status = models.IntegerField(default=0)
    pic_file = models.TextField() 
#=================
class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    enterprise_type = models.SmallIntegerField(blank=True, null=True)
    mobile = models.CharField(unique=True, max_length=50, blank=True, null=True)
    online_status = models.SmallIntegerField(blank=True, null=True)
    password = models.CharField(max_length=64)
    system_source = models.SmallIntegerField(blank=True, null=True)
    user_type = models.SmallIntegerField(blank=True, null=True)
    account = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'user'
        
        
        
class UserLevel(models.Model):
    id = models.BigAutoField(primary_key=True)
    level = models.IntegerField()
    name = models.CharField(max_length=20)
    new_time = models.DateTimeField(blank=True, null=True)
    next_level = models.IntegerField()
    user_id = models.BigIntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'user_level'
        
class UserLevelConfig(models.Model):
    id = models.BigAutoField(primary_key=True)
    fee = models.DecimalField(max_digits=20, decimal_places=2)
    level = models.IntegerField(unique=True)
    max_price = models.IntegerField()
    name = models.CharField(max_length=20)
    next_level = models.IntegerField(unique=True)
    opt_time = models.DateTimeField(auto_now_add=True)
    provide_customer_service = models.SmallIntegerField()
    provide_suggestion = models.SmallIntegerField()
    status = models.SmallIntegerField()
    tag_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user_level_config'
        
        
  
      
class UserAccount(models.Model):
    id = models.BigAutoField(primary_key=True)
    create_time = models.DateTimeField(auto_now_add=True)
    id_card = models.CharField(max_length=20, blank=True, null=True)
    id_card_back_pic = models.CharField(max_length=256, blank=True, null=True)
    id_card_hand_pic = models.CharField(max_length=256, blank=True, null=True)
    id_card_pic = models.CharField(max_length=256, blank=True, null=True)
    mobile = models.CharField(max_length=50, blank=True, null=True)
    opt_id = models.BigIntegerField(blank=True, null=True)
    opt_remark = models.CharField(max_length=256, blank=True, null=True)
    opt_time = models.DateTimeField(blank=True, null=True)
    pay_gestures = models.CharField(max_length=64, blank=True, null=True)
    pay_password = models.CharField(max_length=64, blank=True, null=True)
    real_name = models.CharField(max_length=256, blank=True, null=True)
    status = models.SmallIntegerField()
    update_time = models.DateTimeField(auto_now_add=True)
    user_id = models.BigIntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'user_account'
        
        
        
class FlmAccount(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    fixed_integral = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    available_integral = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    consumption_integral = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    mach_integral = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    original_stock = models.IntegerField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    updat_time = models.DateTimeField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    frozen_integral = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    next_consumption_integral = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    next_sale_integral = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    stock_integral = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    rebate_integral = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    total_team_reward = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    total_sales_reward = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    qdl_team_bonus = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    qdl_sales_bonus = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    jxs_team_bonus = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    jxs_sales_bonus = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    qdl_total = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    qdl_get = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    jxs_total = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    jxs_get = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'flm_account'
 
 

#=========================   



class BankBind(models.Model):
    bank_id = models.CharField(max_length=32, default="")
    bank_name = models.CharField(max_length=32, default="")
    bank_account = models.CharField(max_length=32, default="")
    create_time = models.DateTimeField(auto_now_add =True)
    status = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)
    id_card = models.CharField(max_length=32, default="")
    bank_mobile = models.CharField(max_length=32, default="")
    real_name = models.CharField(max_length=32, default="")
    class Meta:
        managed = False
    
class BankList(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=64)
    rate = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    status = models.IntegerField()

class UserInfo(models.Model):
    user_id = models.IntegerField(default=0)
    job = models.CharField(max_length=250, blank=True, null=True)
    hobby = models.CharField(max_length=250, blank=True, null=True)
    qq = models.CharField(max_length=250, blank=True, null=True)
    wechat = models.CharField(max_length=250, blank=True, null=True)
    email = models.CharField(max_length=250, blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=250, blank=True, null=True)
    emergency_contact_relation = models.CharField(max_length=250, blank=True, null=True)
    emergency_contact_mobile = models.CharField(max_length=250, blank=True, null=True)
    
class Register_user(models.Model):
    mobile = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    register_time = models.DateTimeField(auto_now_add =True)
    user_name = models.CharField(max_length=50)
    status = models.IntegerField(default=0)
    pay_password = models.CharField(max_length=50)
    
class Superuser(models.Model):
    mobile = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
        

class CoinInfo(models.Model):
    gold_num = models.IntegerField(default=0)
    intergral_num = models.FloatField(default=0.0)
    user_id = models.IntegerField(default=0)
    user_level = models.IntegerField(default=1)
    
    
    
class Withdraw_record(models.Model):
    opt_type = models.IntegerField(default=0) #1 intergral  2 gold 
    balance = models.FloatField(default=0.0)
    amount = models.FloatField(default=0.0)
    opt_record = models.CharField(max_length=50)
    opt_time = models.DateTimeField(auto_now_add =True)
    user_id = models.IntegerField(default=0)
    status = models.IntegerField(default=0)# 0未审核 1 通过 -1拒绝



class Tasks(models.Model):
    address = models.CharField(max_length=250)
#     address_province_id = models.IntegerField(default=0)
    total_task_num = models.IntegerField(default=0)
    avali_task_num = models.IntegerField(default=0)
    opt_time = models.CharField(max_length=50)
    status = models.IntegerField(default=0)


class solve_task_user(models.Model):
    province = models.CharField(max_length=250)
    tasks_id = models.IntegerField(default=0)
    get_task_num = models.IntegerField(default=0)
    solve_task_num = models.IntegerField(default=0)
    solve_user_id = models.IntegerField(default=0)
    opt_time = models.DateTimeField(auto_now_add =True)

class Merchant_info(models.Model):
    name = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    mobile = models.CharField(max_length=50)
    industry = models.CharField(max_length=250)
    feature = models.CharField(max_length=250)
    pic_file = models.TextField()
#     pic_file = models.FileField(upload_to="file_upgrade")
    opt_time = models.DateTimeField(auto_now_add =True) 
    upload_user_id = models.IntegerField(default=0)
    status = models.IntegerField(default=0)#-1 驳回 0 未审核 1 审核通过
    remark = models.TextField()

class Area_code(models.Model):
    province = models.CharField(max_length=250)
    num = models.CharField(max_length=250)
    address = models.CharField(max_length=50)
    
class Areas(models.Model):
    areaname = models.CharField(max_length=250)
    parentid = models.CharField(max_length=250)
    shortname = models.CharField(max_length=250)
    
    

    
    

