from django.contrib.auth.models import User, Group

def one_time_startup() :

    name = 'manager'
    try:
        group = Group.objects.get(name=name)
    except Group.DoesNotExist:
        group = Group.objects.create(name=name)
 