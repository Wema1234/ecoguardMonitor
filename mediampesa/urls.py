from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('subscription/',views.subscription,name='subscription'),
    path('payment_form/',views.payment_form,name='payment_form'),
    path('stk_push/',views.stk_push,name='stk_push'),
    path('waiting/<str:transaction_id>/',views.waiting,name='waiting_page'),
    path('callback/',views.callback,name='callback'),
    path('check_status/<int:transaction_id>/',views.check_status,name='check_status'),
    path('payment_success/',views.payment_success,name='payment_success'),
    path('payment_failed/',views.payment_failed,name='payment_failed'),
    path('payment_cancelled/',views.payment_cancelled,name='payment_cancelled'),

]
