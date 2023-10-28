from django.urls import path
from django.conf.urls import url
from . import views



# SET THE NAMESPACE!
app_name = 'rcapp'

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^patient_register/$',views.patient_register,name='patient_register'),
    url(r'^doctor_register/$',views.doctor_register,name='doctor_register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    url(r'^patient_index/$',views.patient_index,name='patient_index'),
    url(r'^doctor_index/$',views.doctor_index,name='doctor_index'),
    url(r'^booking/$',views.booking,name='booking'),
    #url(r'^booking_detail/<int:doctor_id>$',views.booking_detail,name='booking_detail'),
    path('booking_detail/<int:doc_id>', views.booking_detail,name='booking_detail'),
    url(r'^appointment/$',views.appointment,name='appointment'),
]
