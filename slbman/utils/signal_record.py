import django.dispatch
from repository import models
# define single
operation_record = django.dispatch.Signal(providing_args=['time', 'user', 'operation', 'con_name', 'con_ip', 'cmd'])


# register single
def callback(sender,**kwargs):
    try:
        models.OperationLog.objects.create(time=kwargs['time'], user=kwargs['user'], operation=kwargs['operation'],
                                           con_name=kwargs['con_name'], con_ip=kwargs['con_ip'], cmd=kwargs['cmd'])
        # print('添加日志成功')
    except Exception as e:
        print('信号写日志报错: ', str(e))
        pass


operation_record.connect(callback)
