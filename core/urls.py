from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('counter', views.counter, name='counter'),
    path('make-ten', views.make_ten, name='make_ten'),
    path('clock', views.clock, name='clock'),
    path('length-units', views.length_units, name='length_units'),
    path('rmb', views.rmb, name='rmb'),
]
