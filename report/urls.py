from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^all_call/', views.cdr_call, name='all-call'),
    url(r'^general_report/', views.general_report, name='general-report'),
    url(r'^distribution/', views.distribution, name='distribution'),
    url(r'^hangup_cause/', views.hanged_up_cause, name='hangup_cause'),
    url(r'^answered/', views.answered, name='answered'),
    url(r'^unanswered/', views.unanswered, name='unanswered'),
    url(r'^case_report/', views.case_report_range, name='case_report'),
    url(r'^agent_report/', views.agent_report, name='agent_report'),
    url(r'^agent_dashboard/', views.agent_dashboard, name='agent_dashboard'),
    url(r'^settings/', views.settings, name='settings'),
    url(r'^today_setting/', views.today_setting, name='today_setting'),
    url(r'^recorded_calls/', views.recorded_calls, name='recorded_calls'),
    ]

