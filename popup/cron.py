
from django_cron import CronJobBase, Schedule
import glob
from popup.models import Complaint,HoaxTracer
from extension.models import HoaxSetting
from datetime import datetime,date
from django.db.models import Count
from datetime import datetime, timedelta
import os
try:
    from Asterisk import Manager
except ImportError:
    Manager = None

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 120 # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'popup.my_cron_job'    # a unique code

    def do(self):
        hoax_setting_int = HoaxSetting.objects.filter(hoax_type__name="Hoax-Intentional").last()
        hoax_setting_un = HoaxSetting.objects.filter(hoax_type__name="Hoax-Unintentional").last()
        if hoax_setting_int.review_period == "Monthly":
            caller_hoax = Complaint.objects.values("phone").filter(entered_out__month=date.today().month,
                                                                   emergencies__name__in='Hoax-Intentional').annotate(
                num=Count("phone"))
            self.compute(caller_hoax,hoax_setting_int)
        elif hoax_setting_int.review_period == "Weakly":
            dates = date.today()
            start_week = dates - datetime.timedelta(dates.weekday())
            end_week = start_week + datetime.timedelta(7)
            caller_hoax = Complaint.objects.values("phone").filter(entered_out__range=[start_week, end_week],
                                                                   emergencies__name__in='Hoax-Intentional').annotate(
                num=Count("phone"))
            self.compute(caller_hoax, hoax_setting_int)

        if hoax_setting_un.review_period == "Monthly":
            caller_hoax = Complaint.objects.values("phone").filter(entered_out__month=date.today().month,
                                                                   emergencies__name__in='Hoax-Intentional').annotate(
                num=Count("phone"))
            self.compute(caller_hoax,hoax_setting_un)
        elif hoax_setting_int.review_period == "Weakly":
            dates = date.today()
            start_week = dates - datetime.timedelta(dates.weekday())
            end_week = start_week + datetime.timedelta(7)
            caller_hoax = Complaint.objects.values("phone").filter(entered_out__range=[start_week, end_week],
                                                                   emergencies__name__in='Hoax-Intentional').annotate(
                num=Count("phone"))
            self.compute(caller_hoax, hoax_setting_un)

    def compute(self,caller_hoax,hoax_setting):
        manager = Manager.Manager(address=('localhost', 5038), username='smartcall', secret='welcome')
        for rt in caller_hoax:
            if rt['num'] >= int(hoax_setting.number_hoax):
                family = "priority_call"
                key = rt['phone']
                value = 0
                manager.DBPut(family, key, value)
                HoaxTracer.objects.create(number=rt['phone'])

        hoax = HoaxTracer.objects.filter(set_time__gte=datetime.now()-timedelta(days=int(hoax_setting.placed_hoax)))
        for rst in hoax:
            family = "priority_call"
            key = rt.phoned
            value = 1
            manager.DBPut(family, key, value)
