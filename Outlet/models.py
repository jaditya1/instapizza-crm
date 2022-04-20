from django.db import models
from django.contrib.auth.models import User
from Location.models import CountryMaster, StateMaster,CityMaster,AreaMaster
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.safestring import mark_safe
from zapio.settings import MEDIA_URL
from smart_selects.db_fields import ChainedForeignKey
from django.contrib.auth.models import AbstractBaseUser
from Brands.models import Company
from UserRole.models import UserType
from django.contrib.postgres.fields import ArrayField,JSONField
from UserRole.models import ManagerProfile

class OutletProfile(models.Model):
	auth_user = models.OneToOneField(User, on_delete=models.CASCADE,
			related_name='instaoutlet_profile_auth_user', null=True,
								   blank=True)
	Company = models.ForeignKey(Company, related_name='OutletProfile_Company',
												on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'})
	user_type = models.ForeignKey(UserType, related_name='OutletProfile_UserType',
												on_delete=models.CASCADE,verbose_name='User Type',
												limit_choices_to={'active_status':'1'},
												null=True,blank=True)
	username = models.CharField(max_length=100, verbose_name='User Name', unique=True)
	Outletname =  models.CharField(max_length=100, verbose_name='Outlet Name', unique=True)
	mobile_with_isd = models.CharField(max_length=20,
			verbose_name='Mobile No.', unique=True,null=True,
								   blank=True)
	email = models.EmailField(max_length=100, verbose_name='Email Id', unique=True,null=True,
								   blank=True)
	om_pic = models.ImageField(upload_to='om_profile',
								null=True, blank=True, verbose_name='Profile Pic')
	password = models.CharField(max_length=20,
			verbose_name='Password')
	address = models.CharField(max_length=150,verbose_name='Address')
	latitude = models.CharField(max_length=50,verbose_name='Latitude')
	longitude = models.CharField(max_length=50,verbose_name='Longitude')
	city = models.ForeignKey('Location.CityMaster',
		related_name='Outlet_city',on_delete=models.CASCADE,
		verbose_name='City',limit_choices_to={'active_status': '1'}, null=True, blank=True)
	area = models.ForeignKey('Location.AreaMaster',on_delete=models.CASCADE,
		related_name='InstaOutletarea_city',limit_choices_to={"active_status": "1"},null=True, blank=True, 
		verbose_name='Area')
	active_status = models.BooleanField(default=1, verbose_name='Is Active')
	is_open = models.BooleanField(default=1, verbose_name='Is Open')
	is_pos_open = models.BooleanField(default=1, verbose_name='Is Pos Open')
	is_company_active = models.BooleanField(default=1, verbose_name='Is Comapny Active')
	opening_time = models.TimeField(auto_now=False, auto_now_add=False, null=True,blank=True,
											verbose_name="Opening Time")
	closing_time = models.TimeField(auto_now=False, auto_now_add=False, null=True,blank=True,
											verbose_name="Closing Time")
	priority = models.PositiveIntegerField(null=True, blank=True, verbose_name='Priority')
	created_at = models.DateTimeField(auto_now_add=True,
			verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(blank=True, null=True,
			verbose_name='Updation Date & Time')
	check_list = ArrayField(models.TextField(),null=True, blank=True, verbose_name="Check List")
	cam_url = models.CharField(max_length=255,verbose_name='Cam Url', null=True, blank=True)
	pincode = models.IntegerField(verbose_name='Pincode', null=True, blank=True)
	gst = models.CharField(max_length=255,verbose_name='GST', null=True, blank=True)

	def customer_mobile_with_isd(self):
		return "+"+str(self.mobile_with_isd) if self.mobile_with_isd else "-"
	customer_mobile_with_isd.short_description = 'Mobile No. with ISD Code'

	class Meta:
		verbose_name = 'Outlet'
		verbose_name_plural = '  Outlet Profiles'
		unique_together = ('Company', 'priority',)

	def __str__(self):
		return self.Outletname


	def om_picture(self):
		if self.om_pic:
			return mark_safe('<img src='+MEDIA_URL+'%s width="50" height="50" />' % (self.om_pic))
			om_picture.allow_tags = True
		else:
			return 'No Image'
	om_picture.short_description = 'Profile Picture'

class OutletMilesRules(models.Model):
	rule_name = models.CharField(max_length=100, unique=True, verbose_name='Rule Name', db_index=True)
	active_status = models.BooleanField(default=1,verbose_name='Active Status')
	Company = models.ForeignKey(Company, related_name='OutletMilesRules_Company',
												on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'})
	unloaded_miles = models.PositiveIntegerField(verbose_name='Circle Radius in Kms')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created Date & Time') #new added
	updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated Date & Time')

	class Meta:
		verbose_name = "Circle Radius Rule"
		verbose_name_plural = "   Outlet Circle Radius Rule"

	def __str__(self):
		return str(self.rule_name)


class DeliveryBoy(models.Model):
	outlet = ArrayField(models.TextField(),null=True, blank=True, verbose_name="Outlet Mapped Ids")
	name = models.CharField(max_length=100, verbose_name='Name')
	email = models.EmailField(max_length=100, verbose_name='Email Id', unique=True,
																null=True,blank=True)
	profile_pic = models.ImageField(upload_to='deliveryboy_profile',
										null=True, blank=True, verbose_name='Profile Pic')
	mobile = models.CharField(max_length=20,
										verbose_name='Mobile', null=True,blank=True)
	address = models.CharField(max_length=150,verbose_name='Address')
	Company = models.ForeignKey(Company, related_name='DeliveryBoy_Company',null=True, blank=True,
									on_delete=models.CASCADE,verbose_name='Company',
									limit_choices_to={'active_status':'1'})
	active_status = models.BooleanField(default=1, verbose_name='Is Active')
	is_assign = models.BooleanField(default=0, verbose_name='Is Assigned')
	created_at = models.DateTimeField(auto_now_add=True,
														verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(blank=True, null=True,
														verbose_name='Updation Date & Time')
	
	class Meta:
		verbose_name = 'DeliveryBoy'
		verbose_name_plural = 'Delivery Person Details'

	def _str_(self):
		return self.name

	def om_picture(self):
		if self.om_pic:
			return mark_safe('<img src='+MEDIA_URL+'%s width="50" height="50" />' % (self.om_pic))
			om_picture.allow_tags = True
		else:
			return 'No Image'
	om_picture.short_description = 'Profile Picture'



class TempTracking(models.Model):
	Company = models.ForeignKey(Company, related_name='TempTracking_Company',
												on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'})
	outlet = models.ForeignKey(OutletProfile, related_name='TempTracking_outlet',
												on_delete=models.CASCADE,verbose_name='Outlet',
												limit_choices_to={'active_status':'1'})
	staff = models.ForeignKey(ManagerProfile, related_name='TempTracking_staff',
												on_delete=models.CASCADE,verbose_name='Staff Mmeber',
												limit_choices_to={'active_status':'1'})
	body_temp = models.FloatField(verbose_name='Body Temp in F')
	SPO2 = models.FloatField(verbose_name='Oxygen Saturation',null=True, blank=True)
	is_latest = models.BooleanField(default=1, verbose_name='Is Latest')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created Date & Time') #new added
	updated_at = models.DateTimeField(null=True, blank=True, verbose_name='Updated Date & Time')

	class Meta:
		verbose_name = "Staff Temperature Tracking"
		verbose_name_plural = "   Staff Temperature Tracking"


class Crustflix_Videos(models.Model):
	title = models.CharField(max_length=150,verbose_name='Title',blank=True, null=True)
	youtube_url = models.URLField(max_length=300,verbose_name='Youtube URL')
	active_status = models.BooleanField(default=0,verbose_name='Is Active')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created Date & Time')
	updated_at = models.DateTimeField(blank=True, null=True,
			verbose_name='Updation Date & Time')
	class Meta:
		verbose_name = "Crustflix Videos"
		verbose_name_plural = " Crustflix Videos"