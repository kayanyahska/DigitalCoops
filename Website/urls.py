from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^categorize/(?P<arg>[\w\-]+)/$', views.categorize, name='categorize'),
    url(r'^browsehome/$', views.browsehome, name='browsehome'),
	url(r'^item_details/(?P<pk>[0-9]+)/$', views.item_details, name='item_details'),
	# url(r'^register/$', views.register.as_view(), name='register'),
	#url(r'^login/$', views.user_login, name='user_login'),
	url(r'^add_to_cart/(?P<pk>[0-9]+)/$', views.add_to_cart, name='add_to_cart'),
	url(r'^show_cart/$', views.get_cart, name='show_cart'),
	url(r'^remove_from_cart/(?P<pk>[0-9]+)/$', views.remove_from_cart, name='remove_from_cart'),
	url(r'^thanks_buy/(?P<pk>[0-9]+)/$', views.thanks_buy, name='thanks_buy'),
	url(r'^thanks_cart/(?P<cost>[0-9]+)/$', views.thanks_cart, name='thanks_cart'),
	url(r'^clear_cart/$', views.clear_cart, name='clear_cart'),
	url(r'^contact_us', views.contact_us, name='contact_us'),
    url(r'^search/$', views.search, name='search'),
    url(r'^viewHistory/$', views.viewHistory, name='viewHistory'),
    url(r'^administration/$', views.administration, name='administration'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^delete_product/(?P<pk>[0-9]+)/$', views.delete_product, name='delete_product'),
    url(r'^edit_product/(?P<pk>[0-9]+)/$', views.edit_product, name='edit_product'),
    url(r'^sell_history/$', views.sell_history, name='sell_history'),
]
