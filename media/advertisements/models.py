
from django.db import models
from django.contrib.auth.models import User,Group
import datetime
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User as Usertest
# Create your models here.


class Language(models.Model):
    lang_name = models.CharField(max_length = 255)
    lang_code = models.CharField(max_length = 255)
    lang_code = models.CharField(max_length = 150)
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return self.lang_name


class State(models.Model):
    state_name = models.CharField(max_length = 255)
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return self.state_name

class District(models.Model):
    state_id=models.ForeignKey(State,on_delete=models.CASCADE)
    district_name = models.CharField(max_length = 255)
    district_id=models.IntegerField()
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return self.district_name

class City(models.Model):
    city_name = models.CharField(max_length = 255)
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return self.city_name

# def get_image_filename(instance,filename):
#     user_id = 3
#     return 'media/'+'user_photo/'+str(user_id)+

class ProductUnit(models.Model):
    unit_name = models.CharField(max_length = 255)
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return self.unit_name

class UserLinkage(models.Model):
    retailer_user_id= models.ForeignKey(User, on_delete=models.CASCADE,related_name='to_user_retailer')
    wholesaler_user_id= models.ForeignKey(User, on_delete=models.CASCADE,related_name='to_user_wholsaler')
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())
    status = models.IntegerField(default=1)
    def __str__(self):
        return str(self.retailer_user_id)

def get_image_filename(instance,filename):
    user_id=instance.user.id
    print("userr_id",user_id)
    return 'media/'+str(user_id)+'/'+str(filename)


class UserProfile(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    parent_id=models.IntegerField()
    company_name=models.CharField(max_length=255,null=True, blank=True)
    user_type = models.ForeignKey(Group, on_delete=models.CASCADE)
    language= models.ForeignKey(Language, on_delete=models.CASCADE)
    aadhar_no=models.CharField(max_length=255)
    state=models.ForeignKey(State, on_delete=models.CASCADE)
    city=models.CharField(max_length=255,null=True, blank=True)
    district=models.ForeignKey(District, on_delete=models.CASCADE)
    pincode=models.IntegerField(null=True, blank=True)
    address=models.TextField(null=True, blank=True)
    user_photo=models.ImageField(upload_to=get_image_filename,blank=True) #'media/'+'user_photo/'+'2/',blank=True
    aadhar_card=models.ImageField(upload_to=get_image_filename,blank=True)
    pan_card=models.ImageField(upload_to=get_image_filename,blank=True)
    vote_id=models.ImageField(upload_to=get_image_filename,blank=True)
    soil_card=models.ImageField(upload_to=get_image_filename,blank=True)
    fertilizer_photo=models.ImageField(upload_to=get_image_filename,blank=True)
    gst_photo=models.ImageField(upload_to=get_image_filename,blank=True)
    land_area=models.CharField(max_length=255,null=True, blank=True)
    otp=models.CharField(max_length=10,null=True, blank=True)
    fcm_id=models.TextField(null=True, blank=True)
    fms_id=models.CharField(max_length=255,null=True, blank=True)
    gst_number=models.CharField(max_length=255,null=True, blank=True)
    fertilizer_licence=models.CharField(max_length=255,null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return str(self.user_type)

class Product(models.Model):
    product_name = models.CharField(max_length = 255)
    product_code = models.CharField(max_length = 100)
    product_unit_name = models.CharField(max_length = 255,blank=True)
    product_unit = models.CharField(max_length = 10)
    product_price = models.FloatField(null=True, blank=True)
    product_image = models.ImageField(upload_to='media',blank=True)
    total_price = models.FloatField(null=True, blank=True)
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return str(self.id)

    # class Meta:
    #     db_table='tbl_product'

class Order(models.Model):
    user_id_farmer_id= models.ForeignKey(User, on_delete=models.CASCADE,related_name='to_user')
    user_id_retailer_id= models.ForeignKey(User, on_delete=models.CASCADE,related_name='from_user')
    total_price = models.FloatField(null=True, blank=True)
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return str(self.id)

    # class Meta:
    #     db_table='tbl_order'

class ManageContent(models.Model):
    title_eng=models.CharField(max_length=255)
    title_hnd=models.CharField(max_length=255)
    date=models.DateTimeField(default=datetime.datetime.now())
    #state=models.ForeignKey(State,on_delete=models.CASCADE)
    state_id=models.IntegerField(default=0)
    #district=models.ForeignKey(District,on_delete=models.CASCADE)
    district_id=models.IntegerField(default=0)
    #group=models.ForeignKey(Group,on_delete=models.CASCADE)
    group_id=models.CharField(max_length=255)
    contains_eng=models.TextField()
    contains_hnd=models.TextField()
    user_id_admin_id=models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())
    feature_image=models.ImageField(upload_to='media',blank=True)
    def __str__(self):
        return str(self.id)


class Notification(models.Model):
    group_id=models.CharField(max_length=255,blank=True)
    state_id=models.IntegerField(default=0)
    district_id=models.IntegerField(default=0)
    title_eng=models.TextField(blank=True)
    title_hnd=models.TextField(blank=True)
    message_eng=models.TextField(blank=True)
    message_hnd=models.TextField(blank=True)
    sms_status = models.IntegerField(default=0)
    push_status = models.IntegerField(default=0)
    sms_request=models.TextField()
    push_request=models.TextField()
    sms_response=models.TextField()
    push_response=models.TextField()
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())
    status = models.IntegerField(default=1)
    def __str__(self):
        return str(self.id)

class Support(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    subject=models.CharField(max_length=255)
    query=models.CharField(max_length=255)
    check_status = models.IntegerField(default=0)
    created_at =models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return str(self.id)

class SupportReply(models.Model):
    support_id=models.ForeignKey(Support,on_delete=models.CASCADE)
    reply=models.TextField()
    user_id_admin_id=models.ForeignKey(User,on_delete=models.CASCADE)
    query=models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return str(self.support_id)


class Recharge(models.Model):
    user_id_farmer_id= models.ForeignKey(User, on_delete=models.CASCADE,related_name='to_user_auth_recharge')
    user_id_retailer_id= models.ForeignKey(User, on_delete=models.CASCADE,related_name='from_user_auth_recharge')
    amount=models.CharField(max_length=255)
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    transation_id=models.IntegerField()
    transation_request=models.TextField()
    transation_response=models.TextField()
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return str(self.id)

class MobileLang(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    lang_id=models.IntegerField()
    lang_key=models.CharField(max_length=255)
    lang_lab=models.TextField()
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return str(self.user)

class Scratch(models.Model):
    user_id_farmer_id= models.ForeignKey(User, on_delete=models.CASCADE,related_name='to_user_auth')
    user_id_retailer_id= models.ForeignKey(User, on_delete=models.CASCADE,related_name='from_user_auth')
    order=models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.FloatField()
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return str(self.id)


class OrderProductsDetail(models.Model):
    order= models.ForeignKey(Order, on_delete=models.CASCADE)
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    product_quantity =models.IntegerField()
    product_price = models.FloatField()
    product_total_price=models.FloatField()
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return str(self.order)

class LoyaltyPoints(models.Model):
    loyalty_type= models.CharField(max_length=255)
    loyalty_point= models.IntegerField()
    conversion =models.CharField(max_length=255)
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return str(self.loyalty_type)



class UserLoyaltyPoints(models.Model):
    user_id_farmer_id= models.ForeignKey(User, on_delete=models.CASCADE,related_name='to_user_auth_point')
    user_id_retailer_id= models.ForeignKey(User, on_delete=models.CASCADE,related_name='from_user_auth_point')
    to_user_id=models.IntegerField()
    from_user_id=models.IntegerField()
    loyalty_type= models.CharField(max_length=255)
    loyalty_points_id= models.CharField(max_length=255)
    order=models.IntegerField()
    loyalty_point = models.IntegerField()
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())
    status = models.IntegerField(default=1)
    def __str__(self):
        return str(self.order)


class FarmerRechargeConfiguration(models.Model):
    product= models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity= models.IntegerField()
    recharge_amount =models.IntegerField()
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return str(self.product)


class LanguageContaint(models.Model):
    language= models.ForeignKey(Language, on_delete=models.CASCADE)
    sms_on= models.CharField(max_length=255)
    sms_containt= models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return str(self.sms_on)
