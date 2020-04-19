from django.db import models
from django.contrib.auth.models import User
import datetime

#from django.contrib.contenttypes.models import ContentType

# Create your models here.

class UserProfile(models.Model):
	COURSES = (
		('Btech', 'Btech'),
		('Mtech', 'Mtech'),
		('MCA', 'MCA'),
	)

	ACCOUNTS = (
			('Admin', 'Admin'),
			('Student', 'Student'),
	)	

	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	registration_number = models.IntegerField(default=0)
	wallet_balance = models.FloatField(default=0)
	course = models.CharField(max_length=50, choices=COURSES, default='-')
	category = models.CharField(max_length=50, choices=ACCOUNTS)
	# cart = models.IntegerField(null=True)

	def __str__(self) :
	    return self.user.username


class Category(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

class Item(models.Model):
	# CATEGORIES = (
	# 	('Select category', '-'),
	# 	('Stationary', 'Stationary'),
	# 	('Eatables', 'Eatables'),
	# )

	name = models.CharField(max_length=50)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	quantity = models.IntegerField()
	pic = models.FileField(upload_to = 'images/', null=True, blank=True)
	specs = models.TextField()
	unit_price = models.IntegerField()
	item_id = models.IntegerField(primary_key=True)
	
	def __str__(self):
		return self.name 

	@property
	def status(self):
		if self.quantity:
			return True
		return False


class CartItem(models.Model):
	cart_present = models.ForeignKey(User, on_delete=models.CASCADE)
	item = models.ForeignKey(Item, on_delete=models.CASCADE)

	def __str__(self):
		return self.item.name


class Transactions(models.Model):
	transaction_id = models.IntegerField(primary_key=True)
	user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
	transaction_date = models.DateField(null=True, default=datetime.date.today)
	items_included = models.IntegerField()

	def __str__(self):
		return str(self.pk)


class ItemSold(models.Model):
	selling_id = models.IntegerField(primary_key=True)
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	transaction = models.ForeignKey(Transactions, on_delete=models.CASCADE)
	sell_date = models.DateField(null=True, default=datetime.date.today)

	def __str__(self):
		return self.item.name

class Review(models.Model):
	title = models.CharField(max_length=30)
	body = models.TextField()
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
	review_date = models.DateField(null=True)

	def __str__(self):
		return self.title