from django.urls import path,include
from django.contrib import admin

from . import views
urlpatterns = [

    path('',views.index,name='index'),
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('kontaktai/', views.kontaktai, name='kontaktai'),
    path('paieska/', views.paieska, name='paieska'),
    path(r'^i18n/', include('django.conf.urls.i18n')),
    path('/code',views.code,name='code'),

    path('profilis/', views.profilis, name='profilis'),
    path('profilis/ikelimas/', views.ikelimas, name='ikelimas'),
    path('profilis/ikelimas/sukurimas',views.pardavejas_kurimas,name='pardavejo_kurimas'),

    path('prekes/', views.prekes, name='prekes'),
    path('prekes/<int:preke_id>', views.preke, name='preke'),

    path('krepselis/<int:id>', views.KrepselisDetailView.as_view(), name='krepselis'),
    path('krepselis/<int:id>/delete', views.KrepsDelete, name='krepselis_delete'),
    # path('krepselis/<int:id>/update',views.KrepsUpdate, name='krepselis_update'),
    path('krepselis/<int:id>/pirkimas', views.pirkimas,name='krepselis_pirkimas'),

    path('pardavejai/', views.PardavejasListView.as_view(), name='pardavejai'),
    path('pardavejai/<int:pardavejas_id>', views.Pardavejo_prekes, name='pardavejas'),
]

