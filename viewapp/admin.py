from django.contrib import admin
from viewapp import models


# Register your models here.


class Scenery(admin.ModelAdmin):
    list_display = ('id', 'scenery', 'city', 'scenery_detail')
    search_fields = ['scenery', 'city']


class SceneryDetail(admin.ModelAdmin):
    list_display = ('id', 'scenery_name', 'scenery_detail', "scenery_other", 'city', 'mark', 'rank')
    search_fields = ['scenery_name', 'city']


class SceneryWeb(admin.ModelAdmin):
    list_display = (
        'id', 'scenery_name', 'scenery_detail', 'mark', 'rank', 'scenery_address', 'scenery_way', 'scenery_menpiao',
        'scenery_other')
    search_fields = ['scenery_name', 'city']


class HotCity(admin.ModelAdmin):
    list_display = ('id', 'city', 'many_people', 'city_detail', 'city_image')
    search_fields = ['many_people', 'city']


class Soption(admin.ModelAdmin):
    list_display = ('id', 'user', 'create_time', 'update_time')
    search_fields = ['user', 'create_time']


class Woption(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'user', 'create_time', 'update_time')
    search_fields = ['user_id', 'user', 'create_time']


class Way(admin.ModelAdmin):
    list_display = ('id', 'scenerys', 'start_time', 'days', 'say_people', 'is_on')
    search_fields = ['start_time', 'days']


admin.site.site_header = '后台管理'
admin.site.register(models.SceneryAll, Scenery)
admin.site.register(models.SceneryDetail, SceneryDetail)
admin.site.register(models.ScenerySee, SceneryWeb)
admin.site.register(models.OptionScenery, Soption)
admin.site.register(models.OptionWay, Woption)
admin.site.register(models.Ways, Way)
