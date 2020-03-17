from django.db import models


class ServiceToSlb(models.Model):
    service_name = models.CharField(max_length=256)
    vg_id = models.CharField(max_length=256)
    tag = models.CharField(max_length=256, blank=True, null=True)
    slb_id = models.CharField(max_length=256)
    group = models.CharField(max_length=16)

    class Meta:
        managed = False
        db_table = 'service_to_slb'


class SlbInfo(models.Model):
    ecs_id = models.CharField(max_length=256)
    weight = models.IntegerField()
    ecs_ip = models.CharField(max_length=64)
    port = models.IntegerField()
    vg_id = models.CharField(max_length=256)
    stats = models.CharField(max_length=16)
    health = models.CharField(max_length=64, blank=True, null=True)
    slb_id = models.CharField(max_length=256)

    class Meta:
            managed = False
            db_table = 'slb_info'


class SlbUser(models.Model):
    name = models.CharField(max_length=64)
    group = models.CharField(max_length=64)
    stats = models.CharField(max_length=16)
    tag = models.CharField(max_length=64, blank=True, null=True)
    permission_level = models.CharField(max_length=16, blank=True, null=True)  # （'1'管理员， '2'普通用户）

    class Meta:
        managed = False
        db_table = 'slb_user'


class SlbGroup(models.Model):
    name = models.CharField(max_length=64)
    tag = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'slb_group'


class SlbRecords(models.Model):
    user = models.CharField(max_length=64, blank=True, null=True)
    operation = models.CharField(max_length=64, blank=True, null=True)   # 上/下负载
    service_name = models.CharField(max_length=256, blank=True, null=True)  # 服务英文名称
    tag = models.CharField(max_length=64, blank=True, null=True)  # 服务中文名称
    ip = models.CharField(max_length=64, blank=True, null=True)  # 机器IP
    status = models.CharField(max_length=16, blank=True, null=True)  # 操作成功/失败
    time = models.CharField(max_length=256, blank=True, null=True)  # 操作时间

    class Meta:
        managed = False
        db_table = 'slb_records'


class DcUser(models.Model):
    user_name = models.CharField(max_length=64)
    chinese_name = models.CharField(max_length=64, blank=True, null=True)
    add_time = models.CharField(max_length=64, blank=True, null=True)
    tel = models.CharField(max_length=16)
    email = models.CharField(max_length=64)
    stats = models.CharField(max_length=16)
    tag = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dc_user'


class DcmUser(models.Model):
    user_name = models.CharField(max_length=64)
    family_name = models.CharField(max_length=16)
    given_name = models.CharField(max_length=16)
    tel_number = models.CharField(max_length=16)
    email = models.CharField(max_length=64)
    working_place = models.CharField(max_length=256)
    vpn = models.IntegerField()
    password = models.CharField(max_length=256)
    tag = models.IntegerField()  # 标记用户状态 (0 用户正常,-1 用户禁用)
    add_time = models.CharField(max_length=16)  # 用户添加日期

    class Meta:
        managed = False
        db_table = 'dcm_user'


class Ecs(models.Model):
    instance_id = models.CharField(unique=True, max_length=64)
    instance_name = models.CharField(max_length=64)
    sn = models.CharField(max_length=64)
    cpu = models.IntegerField()
    memory = models.IntegerField()
    available = models.IntegerField()
    os_type = models.CharField(max_length=10)
    os_name = models.CharField(max_length=64)
    hostname = models.CharField(max_length=64)
    creation_time = models.CharField(max_length=32)
    region_id = models.CharField(max_length=16)
    instance_type = models.CharField(max_length=32)
    instance_ip = models.CharField(max_length=15)
    instance_mac = models.CharField(max_length=24)
    service_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ecs'


class EcsDisk(models.Model):
    instance_id = models.CharField(max_length=32)
    device = models.CharField(max_length=16)
    size = models.IntegerField()
    creation_time = models.CharField(max_length=16)
    status = models.CharField(max_length=8)
    category = models.CharField(max_length=32)
    region_id = models.CharField(max_length=16)
    disk_id = models.CharField(unique=True, max_length=32)

    class Meta:
        managed = False
        db_table = 'ecs_disk'


class CdnFreshRecord(models.Model):
    fresh_content = models.CharField(max_length=256)
    fresh_type = models.CharField(max_length=64)
    fresh_time = models.CharField(max_length=64)
    stats = models.CharField(max_length=16)
    tag = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cdn_fresh_record'


class Vpn(models.Model):
    user_name = models.CharField(max_length=64)
    vpn_stat = models.IntegerField()  # ( '0'禁用，'1'可用， '2'过期 )
    overtime = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vpn'

