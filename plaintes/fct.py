from django.contrib.auth.models import User, Group

def one_time_startup() :

    liste = ['manager','colis','colis_admin','resa','resa_admin','scan','scan_admin']
    for name in liste : 
        try:
            group = Group.objects.get(name=name)
        except Group.DoesNotExist:
            group = Group.objects.create(name=name)