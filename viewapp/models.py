from django.db import models


# Create your models here.


class SceneryAll(models.Model):
    scenery = models.CharField(max_length=45)
    city = models.CharField(max_length=45)
    scenery_detail = models.CharField(max_length=255)
    image_name = models.CharField(max_length=45)

    class Meta:
        db_table = 'scenery'
        verbose_name = '城市景点'
        verbose_name_plural = verbose_name


class SceneryDetail(models.Model):
    scenery_name = models.CharField(max_length=45)
    city = models.CharField(max_length=45)
    scenery_detail = models.CharField(max_length=255)
    scenery_other = models.CharField(max_length=255)
    mark = models.CharField(max_length=25)
    rank = models.CharField(max_length=80)

    class Meta:
        db_table = 'scenery_detail'
        verbose_name = '景点详情'
        verbose_name_plural = verbose_name


class ScenerySee(models.Model):
    scenery_name = models.CharField(max_length=45)
    scenery_detail = models.CharField(max_length=255)
    mark = models.CharField(max_length=25)
    rank = models.CharField(max_length=80)
    scenery_address = models.CharField(max_length=255)
    scenery_way = models.CharField(max_length=255)
    scenery_open = models.CharField(max_length=255)
    scenery_menpiao = models.CharField(max_length=255)
    scenery_other = models.CharField(max_length=255)

    class Meta:
        db_table = 'scenery_web'
        verbose_name = '景点介绍'
        verbose_name_plural = verbose_name


class HotCity(models.Model):
    city = models.CharField(max_length=45)
    many_people = models.IntegerField()
    city_image = models.CharField(max_length=45)
    city_detail = models.CharField(max_length=255)

    class Meta:
        db_table = 'hot_city'
        verbose_name = '热门城市'
        verbose_name_plural = verbose_name


class OptionScenery(models.Model):
    user_id = models.CharField(max_length=45)
    user = models.CharField(max_length=45)
    options = models.CharField(max_length=255)
    scenery = models.CharField(max_length=45)
    options_time = models.CharField(max_length=55)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'scenery_option'
        verbose_name = '景点评论管理'
        verbose_name_plural = verbose_name


class OptionWay(models.Model):
    user_id = models.CharField(max_length=45)
    user = models.CharField(max_length=45)
    options = models.CharField(max_length=255)
    is_on = models.CharField(max_length=25)
    option_time = models.CharField(max_length=45)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'way_option'
        verbose_name = '路线评论管理'
        verbose_name_plural = verbose_name


class Ways(models.Model):
    scenerys = models.CharField(max_length=85)
    start_time = models.CharField(max_length=85)
    days = models.CharField(max_length=45)
    say_people = models.IntegerField()
    is_on = models.CharField(max_length=45)

    class Meta:
        db_table = 'all_way'
        verbose_name = '路线管理'
        verbose_name_plural = verbose_name


class WayInfo(models.Model):
    address = models.CharField(max_length=85)
    date = models.CharField(max_length=85)
    is_on = models.CharField(max_length=45)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ways_info'
        verbose_name = '路线详情'
        verbose_name_plural = verbose_name


class WayScenery(models.Model):
    address = models.CharField(max_length=85)
    date = models.CharField(max_length=85)
    scenery = models.CharField(max_length=255)
    mark = models.CharField(max_length=45)
    is_on = models.CharField(max_length=45)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ways_scenery'
        verbose_name = '路线景区'
        verbose_name_plural = verbose_name


class UserWay(models.Model):
    city = models.CharField(max_length=85)
    date = models.CharField(max_length=85)
    scenery = models.CharField(max_length=255)
    mark = models.CharField(max_length=85)
    user = models.CharField(max_length=85)
    say_people = models.CharField(max_length=85)
    is_web = models.CharField(max_length=85)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_way'
        verbose_name = '用户自定义路线管理'
        verbose_name_plural = verbose_name


class UserWays(models.Model):
    scenerys = models.CharField(max_length=85)
    user = models.CharField(max_length=85)
    start_time = models.CharField(max_length=85)
    end_time = models.CharField(max_length=85)
    days = models.CharField(max_length=45)
    say_people = models.IntegerField()
    is_on = models.CharField(max_length=45)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_way_detail'
        verbose_name = '用户路线管理'
        verbose_name_plural = verbose_name


class UserInfo(models.Model):
    user = models.CharField(max_length=45)
    name = models.CharField(max_length=45)
    sex = models.CharField(max_length=25)
    phone = models.CharField(max_length=35)
    email = models.CharField(max_length=85)
    myself = models.CharField(max_length=255)
    good_at = models.CharField(max_length=255)
    go_way = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_info'
        verbose_name = '用户信息管理'
        verbose_name_plural = verbose_name


class UserSafe(models.Model):
    user_id = models.CharField(max_length=25)
    user_name = models.CharField(max_length=85)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_safe'
        verbose_name = '账号安全管理'
        verbose_name_plural = verbose_name


class UserScenery(models.Model):
    user = models.CharField(max_length=85)
    scenery = models.CharField(max_length=85)
    city = models.CharField(max_length=85)
    mark = models.CharField(max_length=85)
    rank = models.CharField(max_length=85)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_scenery'
        verbose_name = '用户收藏景区管理'
        verbose_name_plural = verbose_name


class SceneryAdds(models.Model):
    city = models.CharField(max_length=85)
    scenery = models.CharField(max_length=85)
    location = models.CharField(max_length=120)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'scenery_adds'
        verbose_name = '景区经纬度管理'
        verbose_name_plural = verbose_name
