# from django.db import models
# from django.contrib.auth.models import User
# from django.core.validators import MinValueValidator, MaxValueValidator
# from django.utils.safestring import mark_safe
# from zapio.settings import MEDIA_URL
# from smart_selects.db_fields import ChainedForeignKey
# from django.contrib.auth.models import AbstractBaseUser
# from Brands.models import Company

# class Microservice(models.Model):
# 	auth_user = models.OneToOneField(User, on_delete=models.CASCADE,
# 			related_name='Microservice_auth_user', null=True,
# 								   blank=True)
# 	company = models.ForeignKey(Company, related_name='Microservice_Company',
# 												on_delete=models.CASCADE,verbose_name='Company',
# 												limit_choices_to={'active_status':'1'})
# 	username = models.CharField(max_length=100, verbose_name='User Name', unique=True)
# 	password = models.CharField(max_length=20,verbose_name='Password')
# 	active_status = models.BooleanField(default=0, verbose_name='Is Active')
# 	created_at = models.DateTimeField(auto_now_add=True,
# 														verbose_name='Creation Date & Time')
# 	updated_at = models.DateTimeField(blank=True, null=True,
# 														verbose_name='Updation Date & Time')

	
# 	class Meta:
# 		verbose_name = 'MicroService'
# 		verbose_name_plural = ' Microservice'

# 	def __str__(self):
# 		return self.username


# 	def profile_picture(self):
# 		if self.profile_pic:
# 			return mark_safe('<img src='+MEDIA_URL+'%s width="50" height="50" />' % (self.profile_pic))
# 			profile_pic.allow_tags = True
# 		else:
# 			return 'No Image'
# 	profile_picture.short_description = 'Profile Picture'
