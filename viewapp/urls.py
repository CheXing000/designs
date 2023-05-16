from django.urls import path
from viewapp import views

urlpatterns = [
    path('', views.views_page),
    path('views/', views.views_page),
    path('login/', views.login_page),
    path('index/', views.index_page),
    path('people_page/', views.people_page),
    path('people/', views.people),
    path('new_page/', views.page_new),
    path('scenery/', views.scenery_page),
    path('photo/', views.photo_page),
    path('hot-city/', views.hot_page),
    path('text/', views.option_page),
    path('option_page/', views.option_page),
    path('hot_way/', views.hot_way),
    path('way_info/', views.way_info),
    path('way_option/', views.way_option),
    path('make_way/', views.make_way),
    path('save_way/', views.save_ways),
    path('save_scenery/', views.save_scenery),
    path('user_safe/', views.user_safe),
    path('map/',views.map),
    path('logout/',views.logouts),
    path('scenery_data/',views.SceneryView.as_view()),
    path('scenery_datas/',views.ScenerysView.as_view()),
    path('way_data/',views.WayView.as_view()),
    path('add_userway/',views.UserwayView.as_view()),
    path('user_save_way/',views.user_save_way)
]
