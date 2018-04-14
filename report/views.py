from django.shortcuts import render
from .models import Cdr, Queue, QueryTable
from django.db.models import Sum, F, Count
from  .forms import SearchForm, SetForm
from popup.models import Complaint, AgentDispatch, AgentBreak
import collections
import calendar
from extension.models import AgentConf
import datetime
import glob
import os
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
# Create your views here.
# import requests
import time

def general_report(request):
    call_count = Cdr.objects.count()
    unanswered_call = Cdr.objects.filter(disposition="NO ANSWER").count()
    answered_call = Cdr.objects.filter(disposition="ANSWERED").count()
    failed_call = Cdr.objects.filter(disposition="FAILED").count()
    categories = []
    data = []
    categories.append("NO ANSWER")
    categories.append("ANSWERED")
    categories.append("FAILED")

    data.append(unanswered_call)
    data.append(answered_call)
    data.append(failed_call)

    context = {"call_count": call_count,
               "answered_call": answered_call,
               "unanswered_call": unanswered_call,
               "failed_call": failed_call,
               "categories": categories,
               "data": data,
               }
    return render(request, "report/general-report.html", context)
def case_report_range(request):
    from datetime import date
    qt = QueryTable.objects.last()

    if qt is None:
        start_date = "2017-01-01 00:00:00"
        end_date = "{}-{}-{} 23:59:00".format(date.today().year, date.today().month, date.today().day)
    else:
        start_date = '{}-{}-{} {}:{}:00'.format(qt.year_from, qt.month_from, qt.day_from, qt.hour_from, qt.minute_from)
        end_date = '{}-{}-{} {}:{}:00'.format(qt.year_to, qt.month_to, qt.day_to, qt.hour_to, qt.minute_to)


    case_rst_range = Complaint.objects.filter(
        entered_out__range=(start_date, end_date)).count()
    case_agency = Complaint.objects.values('respondent__agency__name').filter(
        entered_out__range=(start_date, end_date)).annotate(num=Count('respondent__agency__name'))
    case_emergency = Complaint.objects.values('emergencies__name').filter(
        entered_out__range=(start_date, end_date)).annotate(num=Count('emergencies__name'))
    case_state = Complaint.objects.values('state__name').filter(
        entered_out__range=(start_date, end_date)).annotate(num=Count('state'))
    case_agent = Complaint.objects.values('agent').filter(
        entered_out__range=(start_date, end_date)).annotate(num=Count('agent'))
    data = []
    categories = []
    data_emergencies = []
    categories_emergency = []
    data_state = []
    categories_state = []
    agent_data = []
    categories_agent = []
    ikey = 0
    ikey2 = 0
    ikey3 = 0
    resp_list = []
    emer_list = []
    state_list = []
    for val in case_agency:
        categories.append(val['respondent__agency__name'])
        data.append(val['num'])
        resp_list.append(ikey)
        ikey += 1
    for val in case_emergency:
        categories_emergency.append(val['emergencies__name'])
        data_emergencies.append(val['num'])
        emer_list.append(ikey2)
        ikey2 += 1
    for val in case_state:
        categories_state.append(val['state__name'])
        data_state.append(val['num'])
        state_list.append(ikey3)
        ikey3 += 1
    for val in case_agent:
        categories_agent.append(val['agent'])
        agent_data.append(val['num'])
    context = {
               "categories": categories,"data": data,"categories_emergency":categories_emergency,
            "data_emergencies":data_emergencies,"categories_state":categories_state,"data_state":data_state,
            "categories_agent":categories_agent,"agent_data":agent_data,"resp_list":resp_list,"emer_list":emer_list,
            "state_list":state_list,"start_date":start_date,"end_date":end_date
               }
    return render(request, "report/complaint_report.html", context)

def case_report_day(request):
    case_rst_range = Complaint.objects.filter(entered_out__day=("day")).count()
    case_agency = Complaint.objects.values('respondent__agency__name').filter(
        entered_out__day=("day")).annotate(num=Count('respondent__agency__name'))
    case_emergency = Complaint.objects.values('emergencies__name').filter(
        entered_out__day=("day")).annotate(num=Count('emergencies__name'))
    case_state = Complaint.objects.values('state__name').filter(
        entered_out__day=("day")).annotate(num=Count('state'))
    case_agent = Complaint.objects.values('agent').filter(
        entered_out__day=("day")).annotate(num=Count('agent'))

def case_report_week_day(request):
    case_rst_range = Complaint.objects.filter(entered_out__week_day=("day")).count()
    case_agency = Complaint.objects.values('respondent__agency__name').filter(
        entered_out__week_day=("day")).annotate(num=Count('respondent__agency__name'))
    case_emergency = Complaint.objects.values('emergencies__name').filter(
        entered_out__week_day=("day")).annotate(num=Count('emergencies__name'))
    case_state = Complaint.objects.values('state__name').filter(
        entered_out__week_day=("day")).annotate(num=Count('state'))
    case_agent = Complaint.objects.values('agent').filter(
        entered_out__week_day=("day")).annotate(num=Count('agent'))

def case_report_month(request):
    case_rst_range = Complaint.objects.filter(entered_out__month=("day")).count()
    case_agency = Complaint.objects.values('respondent__agency__name').filter(
        entered_out__month=("day")).annotate(num=Count('respondent__agency__name'))
    case_emergency = Complaint.objects.values('emergencies__name').filter(
        entered_out__month=("day")).annotate(num=Count('emergencies__name'))
    case_state = Complaint.objects.values('state__name').filter(
        entered_out__month=("day")).annotate(num=Count('state'))
    case_agent = Complaint.objects.values('agent').filter(
        entered_out__month=("day")).annotate(num=Count('agent'))

def case_report_year(request):
    case_rst_range = Complaint.objects.filter(entered_out__year=("day")).count()
    case_agency = Complaint.objects.values('respondent__agency__name').filter(
        entered_out__year=("day")).annotate(num=Count('respondent__agency__name'))
    case_emergency = Complaint.objects.values('emergencies__name').filter(
        entered_out__year=("day")).annotate(num=Count('emergencies__name'))
    case_state = Complaint.objects.values('state__name').filter(
        entered_out__year=("day")).annotate(num=Count('state'))
    case_agent = Complaint.objects.values('agent').filter(
        entered_out__year=("day")).annotate(num=Count('agent'))

def cdr_call(request):
    all_calls = Cdr.objects.all()
    return render(request, 'report/report-call.html', {
        'all_calls': all_calls,
    })

def distribution(request):
    from datetime import datetime, date
    unanswered = 0;
    unanswered_by_day={}
    unanswered_by_hrs = {}
    unanswered_by_day_week={}
    answered_by_day = {}
    default_value = 0
    answered_by_hrs = dict.fromkeys(["00", "01", "02", "03", "04", "05", "06", "07","08","09","10", "11", "12",
                                     "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"],default_value)
    unanswered_by_hrs = dict.fromkeys(["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12",
                                     "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"], default_value)
    received_by_hrs = dict.fromkeys(["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12",
                                     "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"], default_value)
    abandoned_by_hrs = dict.fromkeys(["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12",
                                       "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"], default_value)
    transferred_by_hrs = dict.fromkeys(["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12",
                                      "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"], default_value)
    unanswered_by_day_week = dict.fromkeys([0,1,2,3,4,5,6], default_value)
    answered_by_day_week = dict.fromkeys([0,1,2,3,4,5,6], default_value)
    received_by_day_week = dict.fromkeys([0, 1, 2, 3, 4, 5, 6], default_value)
    abandoned_by_day_week = dict.fromkeys([0, 1, 2, 3, 4, 5, 6], default_value)
    transferred_by_day_week = dict.fromkeys([0, 1, 2, 3, 4, 5, 6], default_value)
    # answered_by_hrs = {}
    # answered_by_day_week = {}
    answered_by_month = {}
    unanswered_by_month = {}
    total_time_by_day = {}
    total_hold_by_day = {}
    total_time_by_day_week = dict.fromkeys([0,1,2,3,4,5,6], default_value)
    total_hold_by_day_week = dict.fromkeys([0,1,2,3,4,5,6], default_value)
    # total_time_by_day_week = {}
    # total_hold_by_day_week = {}
    total_time_by_hr = dict.fromkeys(["00", "01", "02", "03", "04", "05", "06", "07","08","09","10", "11", "12",
                                     "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"],default_value)
    total_hold_by_hr = dict.fromkeys(["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12",
                                      "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"], default_value)
    # total_time_by_hr = {}
    # total_hold_by_hr = {}
    total_time_by_month = {}
    total_hold_by_month = {}
    answered_rate = 0
    unanswered_rate = 0
    abandon_rate = 0
    answered = 0
    abandoned = 0
    total_call = 0.0000001
    call_days = []
    call_hours = []
    qt = QueryTable.objects.last()
    agent_lst = []
    agent_number = 0
    if qt is None:
        start_date = "2017-01-01 00:00:00"
        end_date = "{}-{}-{} 23:59:00".format(date.today().year,date.today().month,date.today().day)
    else:
        start_date = '{}-{}-{} {}:{}:00'.format(qt.year_from,qt.month_from,qt.day_from,qt.hour_from,qt.minute_from)
        end_date = '{}-{}-{} {}:{}:00'.format(qt.year_to, qt.month_to, qt.day_to, qt.hour_to, qt.minute_to)
        str_agent = qt.agents[1:-1]
        str_split = str_agent.split(',')
        for str_s in str_split:
            str_cl = str_s.strip()
            agent_lst.append(str_cl[1:-1])

        if agent_lst:
            agent_number = len(filter(None, agent_lst))

    if not agent_number:
        agent_number= AgentConf.objects.count()
        queue_data = Queue.objects.filter(time__range=(start_date,end_date)).order_by('time')
    else:
        queue_data = Queue.objects.filter(time__range=(start_date,end_date),agent__in = agent_lst).order_by('time')


    for row in queue_data:
        date_arr = row.time.split(" ")
        time_arr = date_arr[1].split(":")
        call_day = date_arr[0]
        call_hour = time_arr[0]

        call_days.append(call_day)
        time_call = datetime.strptime(row.time,'%Y-%m-%d %H:%M:%S.%f')
        call_hours.append(call_hour)
        day_of_week = time_call.weekday()
        month_of_year = time_call.today().month
        if row.event == "ABANDON" or row.event == "EXITWITHTIMEOUT" or row.event == "RINGNOANSWER" or row.event == "EXITWITHKEY":
            unanswered += 1
            unanswered_by_day[call_day] = unanswered_by_day.get(call_day,0)+ 1
            unanswered_by_hrs[call_hour] = unanswered_by_hrs.get(str(call_hour), 0) + 1
            unanswered_by_day_week[day_of_week] = unanswered_by_day_week.get(day_of_week,0) + 1
            unanswered_by_month[month_of_year] = unanswered_by_month.get(month_of_year,0) + 1
        elif row.event == "COMPLETECALLER" or row.event == "COMPLETEAGENT":
            answered += 1
            answered_by_day[call_day] = answered_by_day.get(call_day, 0) + 1
            answered_by_hrs[call_hour] = answered_by_hrs.get(str(call_hour), 0) + 1
            answered_by_day_week[day_of_week] = answered_by_day_week.get(day_of_week, 0) + 1
            answered_by_month[month_of_year] = answered_by_month.get(month_of_year, 0) + 1

            total_time_by_day[call_day] = total_time_by_day.get(call_day, 0) + int(row.data2)
            total_hold_by_day[call_day] = total_hold_by_day.get(call_day, 0) + int(row.data1)

            total_time_by_hr[call_hour] = total_time_by_hr.get(call_hour, 0) + int(row.data2)
            total_hold_by_hr[call_hour] = total_hold_by_hr.get(call_hour, 0) + int(row.data1)

            total_time_by_day_week[day_of_week] = total_time_by_day_week.get(day_of_week, 0) + int(row.data2)
            total_hold_by_day_week[day_of_week] = total_hold_by_day_week.get(day_of_week, 0) + int(row.data1)

            total_time_by_month[month_of_year] = total_time_by_month.get(month_of_year, 0) + int(row.data2)
            total_hold_by_month[month_of_year] = total_hold_by_month.get(month_of_year, 0) + int(row.data1)

        if row.event == "ABANDON":
            abandoned_by_hrs[call_hour] = abandoned_by_hrs.get(str(call_hour), 0) + 1
            abandoned_by_day_week[day_of_week] = abandoned_by_day_week.get(day_of_week, 0) + 1
            abandoned += 1

        if row.event == "TRANSFER":
            transferred_by_hrs[call_hour] = transferred_by_hrs.get(str(call_hour), 0) + 1
            transferred_by_day_week[day_of_week] = transferred_by_day_week.get(day_of_week, 0) + 1

        if row.event == "ABANDON" or row.event == "EXITWITHTIMEOUT" or row.event == "COMPLETECALLER" or row.event == "RINGNOANSWER" or row.event == "EXITWITHKEY" or row.event == "TRANSFER"or row.event == "COMPLETEAGENT":
            received_by_hrs[call_hour] = received_by_hrs.get(str(call_hour), 0) + 1
            received_by_day_week[day_of_week] = received_by_day_week.get(day_of_week, 0) + 1
    categories = []
    categories_day_week = []
    data_answered = []
    data_unanswered = []
    data_transferred = []
    data_abandoned = []
    data_received = []
    data_total_hold_by_hr = []
    data_total_talktime_by_hr = []
    data_total_hold_by_hr1 = []
    data_total_talktime_by_hr1 = []
    data_answered_by_day_week = []
    data_unanswered_by_day_week = []
    data_received_by_day_week = []
    data_abandoned_by_day_week = []
    data_transferred_by_day_week = []
    data_total_hold_by_day_week = []
    data_total_time_by_day_week = []
    data_total_hold_by_day_week1 = []
    data_total_time_by_day_week1 = []
    time_period = []
    day_period = []

    a_b_h_ordered = collections.OrderedDict(sorted(answered_by_hrs.items()))
    for key, val in sorted(a_b_h_ordered.iteritems()):
        categories.append("{}:00 - {}:59".format(key,key))
        time_period.append(int(key))
        data_answered.append(val)

    ua_b_h_ordered = collections.OrderedDict(sorted(unanswered_by_hrs.items()))
    for key, val in ua_b_h_ordered.iteritems():
        data_unanswered.append(val)

    rc_b_h_ordered = collections.OrderedDict(sorted(received_by_hrs.items()))
    for key, val in rc_b_h_ordered.iteritems():
        data_received.append(val)

    tr_b_h_ordered = collections.OrderedDict(sorted(transferred_by_hrs.items()))
    for key, val in tr_b_h_ordered.iteritems():
        data_transferred.append(val)

    tra_b_h_ordered = collections.OrderedDict(sorted(abandoned_by_hrs.items()))
    for key, val in tra_b_h_ordered.iteritems():
        data_abandoned.append(val)

    to_b_h_ordered = collections.OrderedDict(sorted(total_hold_by_hr.items()))
    for key, val in to_b_h_ordered.iteritems():
        data_total_hold_by_hr1.append(time.strftime('%H:%M:%S', time.gmtime(val)))
        data_total_hold_by_hr.append(val)

    totalk_b_h_ordered = collections.OrderedDict(sorted(total_time_by_hr.items()))
    for key, val in totalk_b_h_ordered.iteritems():
        data_total_talktime_by_hr1.append(time.strftime('%H:%M:%S', time.gmtime(val)))
        data_total_talktime_by_hr.append(val)

    u_d_w_ordered = collections.OrderedDict(sorted(unanswered_by_day_week.items()))
    for key, val in u_d_w_ordered.iteritems():
        categories_day_week.append(calendar.day_name[key])
        day_period.append(key)
        data_unanswered_by_day_week.append(val)

    a_d_w_ordered = collections.OrderedDict(sorted(answered_by_day_week.items()))
    for key, val in a_d_w_ordered.iteritems():
        data_answered_by_day_week.append(val)

    dar_d_w_ordered = collections.OrderedDict(sorted(received_by_day_week.items()))
    for key, val in dar_d_w_ordered.iteritems():
        data_received_by_day_week.append(val)

    a1_d_w_ordered = collections.OrderedDict(sorted(abandoned_by_day_week.items()))
    for key, val in a1_d_w_ordered.iteritems():
        data_abandoned_by_day_week.append(val)

    tra_d_w_ordered = collections.OrderedDict(sorted(transferred_by_day_week.items()))
    for key, val in tra_d_w_ordered.iteritems():
        data_transferred_by_day_week.append(val)

    tt_d_w_ordered = collections.OrderedDict(sorted(total_time_by_day_week.items()))
    for key, val in tt_d_w_ordered.iteritems():
        data_total_time_by_day_week.append(val)
        data_total_time_by_day_week1.append(time.strftime('%H:%M:%S', time.gmtime(val)))

    th_d_w_ordered = collections.OrderedDict(sorted(total_hold_by_day_week.items()))
    for key, val in th_d_w_ordered.iteritems():
        data_total_hold_by_day_week.append(val)
        data_total_hold_by_day_week1.append(time.strftime('%H:%M:%S', time.gmtime(val)))

    total_call = answered + unanswered
    if total_call == 0:
        total_call = 0.00000001
    answered_rate = round((float(answered)/total_call)*100,2)
    unanswered_rate = round((float(unanswered)/total_call)*100,2)
    abandon_rate = round((float(abandoned)/total_call)*100,2)
    answered_rate = "{} %".format(answered_rate)
    unanswered_rate = "{} %".format(unanswered_rate)
    abandon_rate = "{} %".format(abandon_rate)
    call_days_list = list(set(call_days))
    call_hours_list = list(set(call_hours))
    calldays = call_days_list.sort()
    callhours = call_hours_list.sort()
    context = {"start_date":start_date,"end_date":end_date,"answered":answered, "unanswered":unanswered,
               "abandoned":abandoned, "total_call":int(total_call),"answered_rate":answered_rate, "unanswered_rate":unanswered_rate,
               "abandon_rate":abandon_rate,"categories":categories, "data_answered":data_answered,"data_unanswered":data_unanswered,
               "data_total_talktime_by_hr":data_total_talktime_by_hr,"data_total_hold_by_hr":data_total_hold_by_hr,
               "data_unanswered_by_day_week":data_unanswered_by_day_week, "data_answered_by_day_week":data_answered_by_day_week,
               "categories_day_week":categories_day_week,"data_total_time_by_day_week":data_total_time_by_day_week,
               "data_total_hold_by_day_week":data_total_hold_by_day_week,"data_received":data_received,
               "data_transferred":data_transferred,"time_period":time_period,"data_total_talktime_by_hr1":data_total_talktime_by_hr1,
               "data_total_hold_by_hr1":data_total_hold_by_hr1,"data_abandoned":data_abandoned,"data_received_by_day_week":data_received_by_day_week,
               "data_abandoned_by_day_week":data_abandoned_by_day_week,"data_transferred_by_day_week":data_transferred_by_day_week,
               "day_period":day_period,"data_total_hold_by_day_week1":data_total_hold_by_day_week1,
               "data_total_time_by_day_week1":data_total_time_by_day_week1,"agent_number":agent_number
               }
    return render(request, "report/distribution.html", context)

def hanged_up_cause(request):
    hang_cause = Queue.objects.values('event').filter(event__in=['COMPLETECALLER','COMPLETEAGENT']).annotate(num=Count('event'))
    categories = []
    data = []
    handup_cause = {}
    total_hangup = 0
    for rst in hang_cause:
        handup_cause[rst['event']] = rst['num']
        rst_event = rst['event']
        rst_num = rst['num']
        categories.append(str(rst_event))
        data.append(int(rst_num))
        total_hangup += int(rst_num)

    return render(request, "report/hanged.html", {})



def answered(request):
    from datetime import datetime, date
    total_hold = 0
    total_duration = 0
    total_calls = 0
    total_calls_queue = {}
    transfer_num= 0
    average_hold = 0
    average_duration = 0
    default_value = 0
    ans_time = dict.fromkeys([30, 60, 90, 120, 150, 180,210,240,270,300,301 ], default_value)
    call_time = dict.fromkeys([30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 301], default_value)

    qt = QueryTable.objects.last()
    agent_lst = []
    agent_number = 0
    if qt is None:
        start_date = "2017-01-01 00:00:00"
        end_date = "{}-{}-{} 23:59:00".format(date.today().year,date.today().month,date.today().day)
    else:
        start_date = '{}-{}-{} {}:{}:00'.format(qt.year_from,qt.month_from,qt.day_from,qt.hour_from,qt.minute_from)
        end_date = '{}-{}-{} {}:{}:00'.format(qt.year_to, qt.month_to, qt.day_to, qt.hour_to, qt.minute_to)
        str_agent = qt.agents[1:-1]
        str_split = str_agent.split(',')
        for str_s in str_split:
            str_cl = str_s.strip()
            agent_lst.append(str_cl[1:-1])

        if agent_lst:
            agent_number = len(filter(None, agent_lst))

    if not agent_number:
        agent_number= AgentConf.objects.count()
        answered_rst = Queue.objects.filter(event__in=['COMPLETECALLER', 'COMPLETEAGENT', 'TRANSFER', 'CONNECT'],
                                            time__range=(start_date, end_date)).order_by('time')
    else:
        answered_rst = Queue.objects.filter(event__in=['COMPLETECALLER','COMPLETEAGENT','TRANSFER','CONNECT'],
                                        time__range=(start_date, end_date), agent__in=agent_lst).order_by('time')
    for row in answered_rst:
        if row.event != "TRANSFER" and  row.event !="CONNECT":
            total_hold += int(row.data1)
            total_duration += int(row.data2)
            total_calls += 1
            total_calls_queue[row.queuename] = total_calls_queue.get(row.queuename, 0) + 1
        elif row.event == "TRANSFER":
            transfer_num += 1
        elif row.event == "CONNECT":
            holdtime = int(row.data1)
            if holdtime >= 0 and holdtime <= 30 :
                ans_time[30] = ans_time.get(30, 0) + 1
            elif holdtime >= 31 and holdtime <= 60:
                ans_time[60] = ans_time.get(60, 0) + 1
            elif holdtime >= 61 and holdtime <= 90:
                ans_time[90] = ans_time.get(90, 0) + 1
            elif holdtime >= 91 and holdtime <= 120:
                ans_time[120] = ans_time.get(120, 0) + 1
            elif holdtime >= 121 and holdtime <= 150:
                ans_time[150] = ans_time.get(150, 0) + 1
            elif holdtime >= 151 and holdtime <= 180:
                ans_time[180] = ans_time.get(180, 0) + 1
            elif holdtime >= 181 and holdtime <= 210:
                ans_time[210] = ans_time.get(210, 0) + 1
            elif holdtime >= 211 and holdtime <= 240:
                ans_time[240] = ans_time.get(240, 0) + 1
            elif holdtime >= 241 and holdtime <= 270:
                ans_time[270] = ans_time.get(270, 0) + 1
            elif holdtime >= 271 and holdtime <= 300:
                ans_time[300] = ans_time.get(300, 0) + 1
            elif holdtime >= 301:
                ans_time[301] = ans_time.get(301, 0) + 1
        if row.event == "COMPLETECALLER" or row.event == "COMPLETEAGENT":
            calltime = int(row.data2)
            if calltime >= 0 and calltime <= 30:
                call_time[30] = call_time.get(30, 0) + 1
            elif calltime >= 31 and calltime <= 60:
                call_time[60] = call_time.get(60, 0) + 1
            elif calltime >= 61 and calltime <= 90:
                call_time[90] = call_time.get(90, 0) + 1
            elif calltime >= 91 and calltime <= 120:
                call_time[120] = call_time.get(120, 0) + 1
            elif calltime >= 121 and calltime <= 150:
                call_time[150] = call_time.get(150, 0) + 1
            elif calltime >= 151 and calltime <= 180:
                call_time[180] = call_time.get(180, 0) + 1
            elif calltime >= 181 and calltime <= 210:
                call_time[210] = call_time.get(210, 0) + 1
            elif calltime >= 211 and calltime <= 240:
                call_time[240] = call_time.get(240, 0) + 1
            elif calltime >= 241 and calltime <= 270:
                call_time[270] = call_time.get(270, 0) + 1
            elif calltime >= 271 and calltime <= 300:
                call_time[300] = call_time.get(300, 0) + 1
            elif calltime >= 301:
                call_time[301] = call_time.get(301, 0) + 1
    if total_calls > 0:
        average_hold = total_hold / total_calls
        average_duration = total_duration / total_calls
    total_call = answered_rst.count()
    categories = []
    ans_time_period = []
    call_time_period = []
    duration_t = []
    ans_time_ordered = collections.OrderedDict(sorted(ans_time.items()))
    ikey = 0
    for key, val in ans_time_ordered.iteritems():

        if key == 301:
            categories.append(time.strftime('%H:%M:%S', time.gmtime(key)) + " +")
        else:
            categories.append(time.strftime('%H:%M:%S', time.gmtime(key)))
        ans_time_period.append(val)
        duration_t.append(ikey)
        ikey += 1


    call_time_ordered = collections.OrderedDict(sorted(call_time.items()))
    for key, val in call_time_ordered.iteritems():
        call_time_period.append(val)

    context = {"average_hold":average_hold,"average_duration":average_duration,"categories":categories,
              "ans_time_period":ans_time_period,"total_call":total_call,"call_time_period":call_time_period,
               "duration_t":duration_t, "start_date":start_date,"end_date":end_date,"agent_number":agent_number }

    return render(request, "report/answered.html", context)

def unanswered (request):
    from datetime import datetime, date
    qt = QueryTable.objects.last()
    agent_lst = []
    agent_number = 0
    if qt is None:
        start_date = "2017-01-01 00:00:00"
        end_date = "{}-{}-{} 23:59:00".format(date.today().year, date.today().month, date.today().day)
    else:
        start_date = '{}-{}-{} {}:{}:00'.format(qt.year_from, qt.month_from, qt.day_from, qt.hour_from, qt.minute_from)
        end_date = '{}-{}-{} {}:{}:00'.format(qt.year_to, qt.month_to, qt.day_to, qt.hour_to, qt.minute_to)
        str_agent = qt.agents[1:-1]
        str_split = str_agent.strip().split(',')
        for str_s in str_split:
            str_cl = str_s.strip()
            agent_lst.append(str_cl[1:-1])

        if agent_lst:
            agent_number = len(filter(None, agent_lst))

    if not agent_number:
        agent_number = AgentConf.objects.count()
        unanswered_rst = Queue.objects.filter(event__in=['ABANDON','EXITWITHTIMEOUT'],time__range=(start_date,end_date)).order_by('time')
    else:
        unanswered_rst = Queue.objects.filter(event__in=['ABANDON','EXITWITHTIMEOUT'],time__range=(start_date,end_date),agent__in = agent_lst).order_by('time')
    abandoned = 0
    abandon_end_pos = 0
    abandon_start_pos = 0
    total_hold_abandon = 0
    timeout = 0
    timeout_end_pos = 0
    timeout_start_pos = 0
    total_hold_timeout = 0
    abandon_calls_queue = {}
    abandon_average_hold = 0
    abandon_average_start = 0
    abandon_average_end = 0
    total_abandon = 0
    default_value = 0
    exit_time = dict.fromkeys([30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 301], default_value)
    wait_time = dict.fromkeys([30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 301],
                              default_value)
    for row in unanswered_rst:
        if row.event == "ABANDON":
            cal_wait = int(row.data3.strip())
            abandoned += 1
            # abandon_end_pos += int(row.data1)
            # abandon_start_pos += int(row.data2)
            total_hold_abandon += cal_wait
            waittime = int(row.data3)
            if waittime >= 0 and waittime <= 30:
                wait_time[30] = wait_time.get(30, 0) + 1
            elif waittime >= 31 and waittime <= 60:
                wait_time[60] = wait_time.get(60, 0) + 1
            elif waittime >= 61 and waittime <= 90:
                wait_time[90] = wait_time.get(90, 0) + 1
            elif waittime >= 91 and waittime <= 120:
                wait_time[120] = wait_time.get(120, 0) + 1
            elif waittime >= 121 and waittime <= 150:
                wait_time[150] = wait_time.get(150, 0) + 1
            elif waittime >= 151 and waittime <= 180:
                wait_time[180] = wait_time.get(180, 0) + 1
            elif waittime >= 181 and waittime <= 210:
                wait_time[210] = wait_time.get(210, 0) + 1
            elif waittime >= 211 and waittime <= 240:
                wait_time[240] = wait_time.get(240, 0) + 1
            elif waittime >= 241 and waittime <= 270:
                wait_time[270] = wait_time.get(270, 0) + 1
            elif waittime >= 271 and waittime <= 300:
                wait_time[300] = wait_time.get(300, 0) + 1
            elif waittime >= 301:
                wait_time[301] = wait_time.get(301, 0) + 1
        elif row.event == "EXITWITHTIMEOUT":
            timeout += 1

            cal_wait = int(str(row.data3).strip())
            # timeout_end_pos += int(row.data1)
            # timeout_start_pos += int(row.data2)
            total_hold_timeout += cal_wait
            if cal_wait >= 0 and cal_wait <= 30:
                exit_time[30] = exit_time.get(30, 0) + 1
            elif cal_wait >= 31 and cal_wait <= 60:
                exit_time[60] = exit_time.get(60, 0) + 1
            elif cal_wait >= 61 and cal_wait <= 90:
                exit_time[90] = exit_time.get(90, 0) + 1
            elif cal_wait >= 91 and cal_wait <= 120:
                exit_time[120] = exit_time.get(120, 0) + 1
            elif cal_wait >= 121 and cal_wait <= 150:
                exit_time[150] = exit_time.get(150, 0) + 1
            elif cal_wait >= 151 and cal_wait <= 180:
                exit_time[180] = exit_time.get(180, 0) + 1
            elif cal_wait >= 181 and cal_wait <= 210:
                exit_time[210] = exit_time.get(210, 0) + 1
            elif cal_wait >= 211 and cal_wait <= 240:
                exit_time[240] = exit_time.get(240, 0) + 1
            elif cal_wait >= 241 and cal_wait <= 270:
                exit_time[270] = exit_time.get(270, 0) + 1
            elif cal_wait >= 271 and cal_wait <= 300:
                exit_time[300] = exit_time.get(300, 0) + 1
            elif cal_wait >= 301:
                exit_time[301] = exit_time.get(301, 0) + 1

        abandon_calls_queue[row.queuename] = abandon_calls_queue.get(row.queuename, 0) + 1
    if abandoned > 0:
        abandon_average_hold = total_hold_abandon/abandoned
        # abandon_average_end = abandon_end_pos/abandoned
        # abandon_average_start = abandon_start_pos/abandoned
    total_abandon = abandoned + timeout
    categories = []
    exit_time_period = []
    wait_time_period = []
    duration_t = []
    ikey = 0
    exit_time_ordered = collections.OrderedDict(sorted(exit_time.items()))
    for key, val in exit_time_ordered.iteritems():
        if key == 301:
            categories.append(time.strftime('%H:%M:%S', time.gmtime(key)) + " +")
        else:
            categories.append(time.strftime('%H:%M:%S', time.gmtime(key)))
        exit_time_period.append(val)
        duration_t.append(ikey)
        ikey += 1

    wait_time_ordered = collections.OrderedDict(sorted(wait_time.items()))
    for key, val in wait_time_ordered.iteritems():
        wait_time_period.append(val)

    context = {"abandon_average_hold":abandon_average_hold, "total_abandon":total_abandon,"timeout":timeout,
               "exit_time_period":exit_time_period,"wait_time_period":wait_time_period,
               "categories":categories,"duration_t":duration_t,"agent_number":agent_number,"start_date":start_date,"end_date":end_date}

    return render(request, "report/unanswered.html", context)

def dispatched(request):
    dispatch_rst = AgentDispatch.objects.filter(
        entered_out__range=("start_date", "end_date")).count()
    dispatch_rst_status = AgentDispatch.objects.values('status').filter(
        entered_out__range=("start_date", "end_date")).annotate(num=Count('status'))
    dispatch_dur = AgentDispatch.objects.values('dispatch_duration').filter(
        entered_out__range=("start_date", "end_date"))
    dis_dur = dict.fromkeys(["30", "60", "90", "120", "150", "180", "181+"])

    durtime = int(dispatch_dur['dispatch_duration'])
    if durtime >= 0 and durtime <= 30:
        dis_dur["30"] = dis_dur.get("30", 0) + 1
    elif durtime >= 31 and durtime <= 60:
        dis_dur["60"] = dis_dur.get("60", 0) + 1
    elif durtime >= 61 and durtime <= 90:
        dis_dur["90"] = dis_dur.get("90", 0) + 1
    elif durtime >= 91 and durtime <= 120:
        dis_dur["120"] = dis_dur.get("120", 0) + 1
    elif durtime >= 121 and durtime <= 150:
        dis_dur["150"] = dis_dur.get("150", 0) + 1
    elif durtime >= 151 and durtime <= 180:
        dis_dur["180"] = dis_dur.get("180", 0) + 1
    elif durtime >= 181:
        dis_dur["181+"] = dis_dur.get("181+", 0) + 1

    context = {"durtime": durtime}
    return render(request, "report/dispatcher_analysis.html", context)

def agent_report(request):
    from datetime import date

    agent_dict  = dict.fromkeys(["talktime", "holdtime", "timesession","idle_time", "answered", "unanswered",
                                 "total", "pausetime","sessionpercent"],0.0000001)
    break_dict = dict.fromkeys(["launch", "breakfast", "dinner", "withdrawal", "technical", "restroom","pause_time"], 0.0000001)
    agent_dict_total = dict.fromkeys(
        ["talktime", "holdtime", "timesession", "idle_time", "answered", "unanswered", "total", "pausetime",
         "sessionpercent"], 0.0000001)
    agent_report_total = {}
    agent_report = {}
    agent_break = {}

    qt = QueryTable.objects.last()
    agent_lst = []
    ext_lst = []
    agent_number = 0
    if qt is None:
        start_date = "2017-01-01 00:00:00"
        end_date = "{}-{}-{} 23:59:00".format(date.today().year, date.today().month, date.today().day)
    else:
        start_date = '{}-{}-{} {}:{}:00'.format(qt.year_from, qt.month_from, qt.day_from, qt.hour_from, qt.minute_from)
        end_date = '{}-{}-{} {}:{}:00'.format(qt.year_to, qt.month_to, qt.day_to, qt.hour_to, qt.minute_to)
        str_agent = qt.agents[1:-1]
        str_split = str_agent.split(',')
        for str_s in str_split:
            str_cl = str_s.strip()
            agent_lst.append(str_cl[1:-1])
        if agent_lst:
            agent_number = len(filter(None, agent_lst))

    if not agent_number:
        agent_number = AgentConf.objects.count()
        agenttconf = AgentConf.objects.all()
        agt_report_total = Queue.objects.all()
        answered_rst_total = Queue.objects.filter(
            event__in=['COMPLETECALLER', 'COMPLETEAGENT', 'TRANSFER', 'CONNECT'],
            time__range=(start_date, end_date)).count()
        unanswered_rst_total = Queue.objects.filter(event__in=['ABANDON', 'EXITWITHTIMEOUT'],
                                                    time__range=(start_date, end_date)).count()
    else:
        str_ext = qt.ext[1:-1]
        str_spt = str_ext.split(',')
        for str_s in str_spt:
            str_cl = str_s.strip()
            ext_lst.append(str_cl[1:-1])
        agenttconf = AgentConf.objects.filter(extension__in=ext_lst)
        agt_report_total = Queue.objects.filter(agent__in=agent_lst)
        answered_rst_total = Queue.objects.filter(
            event__in=['COMPLETECALLER', 'COMPLETEAGENT', 'TRANSFER', 'CONNECT'],
            time__range=(start_date, end_date),agent__in=agent_lst).count()
        unanswered_rst_total = Queue.objects.filter(event__in=['ABANDON', 'EXITWITHTIMEOUT'],
                                                    time__range=(start_date, end_date),agent__in=agent_lst).count()
    for agents in agenttconf:
        my_agent = "Agent/{}".format(agents.extension)
        agt_report = Queue.objects.filter(agent = my_agent,time__range=(start_date, end_date))
        for row in agt_report:
            if row.event == "COMPLETECALLER" or row.event == "COMPLETEAGENT":
                if "talktime" in agent_dict:
                    agent_dict["talktime"] += int(row.data2)
            elif row.event == "CONNECT":
                if "holdtime" in agent_dict:
                    agent_dict["holdtime"] += int(row.data1)
            elif row.event == "AGENTLOGOFF":
                if "timesession" in agent_dict:
                    agent_dict["timesession"] += int(row.data2)
        answered_rst = Queue.objects.filter(
            event__in=['COMPLETECALLER', 'COMPLETEAGENT', 'TRANSFER', 'CONNECT'],agent = my_agent,
                                              time__range=(start_date, end_date)).count()
        agent_dict["answered"] = answered_rst
        unanswered_rst = Queue.objects.filter(event__in=['ABANDON', 'EXITWITHTIMEOUT'],agent = my_agent,
                                              time__range=(start_date, end_date)).count()
        agent_dict["unanswered"] = unanswered_rst
        total_calls = agt_report.count()
        agent_dict["total"] = total_calls
        agent_pause = AgentBreak.objects.filter(agent=agents.agent)
        pause_time = datetime.timedelta(seconds=0)
        launch_time = datetime.timedelta(seconds=0)
        breakfast_time = datetime.timedelta(seconds=0)
        dinner_time = datetime.timedelta(seconds=0)
        withdraw_time = datetime.timedelta(seconds=0)
        technical_time = datetime.timedelta(seconds=0)
        restroom_time = datetime.timedelta(seconds=0)
        for ap in agent_pause:
            if not ap.time_spent is None:
                pause_time += ap.time_spent
                if ap.breaks.name == "Launch Break":
                    launch_time += ap.time_spent
                elif ap.breaks.name == "Breakfast":
                    breakfast_time += ap.time_spent
                elif ap.breaks.name == "Dinner":
                    dinner_time += ap.time_spent
                elif ap.breaks.name == "Withdrawal":
                    withdraw_time += ap.time_spent
                elif ap.breaks.name == "Technical":
                    technical_time += ap.time_spent
                elif ap.breaks.name == "Rest Room":
                    restroom_time += ap.time_spent
        agent_dict["pausetime"] =  str(pause_time).split('.', 2)[0]
        break_dict["pause_time"] = str(pause_time).split('.', 2)[0]
        break_dict["launch"] = str(launch_time).split('.', 2)[0]
        break_dict["breakfast"] = str(breakfast_time).split('.', 2)[0]
        break_dict["dinner"] = str(dinner_time).split('.', 2)[0]
        break_dict["withdrawal"] = str(withdraw_time).split('.', 2)[0]
        break_dict["technical"] = str(technical_time).split('.', 2)[0]
        break_dict["restroom"] = str(restroom_time).split('.', 2)[0]
        if "talktime" in agent_dict:
            idle_time = int(agent_dict["timesession"]) - (int(agent_dict["talktime"]) + int(agent_dict["holdtime"]))
            session_percent = round((float(agent_dict["talktime"])/float(agent_dict["timesession"]))*100,2)
            agent_dict["sessionpercent"] = "{} %".format(session_percent)
            agent_dict["talktime"] =  time.strftime('%H:%M:%S', time.gmtime(agent_dict["talktime"]))
            agent_dict["holdtime"] = time.strftime('%H:%M:%S', time.gmtime(agent_dict["holdtime"]))
            agent_dict["timesession"] = time.strftime('%H:%M:%S', time.gmtime(agent_dict["timesession"]))
            agent_dict["idle_time"] = time.strftime('%H:%M:%S', time.gmtime(idle_time))
        agent_name = "{} {}".format(agents.agent.first_name, agents.agent.last_name)
        agent_report[agent_name] = agent_dict
        agent_dict = dict.fromkeys(
            ["talktime", "holdtime", "timesession", "idle_time", "answered", "unanswered", "total", "pausetime",
             "sessionpercent"], 0.0000001)
        agent_break[agent_name] = break_dict
        break_dict = dict.fromkeys(
            ["launch", "breakfast", "dinner", "withdrawal", "technical", "restroom", "pause_time"], 0.0000001)

        # For all the agents
    for row in agt_report_total:
        if row.event == "COMPLETECALLER" or row.event == "COMPLETEAGENT":
            if "talktime" in agent_dict_total:
                agent_dict_total["talktime"] += int(row.data2)
        elif row.event == "CONNECT":
            if "holdtime" in agent_dict_total:
                agent_dict_total["holdtime"] += int(row.data1)
        elif row.event == "AGENTLOGOFF":
            if "timesession" in agent_dict_total:
                agent_dict_total["timesession"] += int(row.data2)

    agent_dict_total["answered"] = answered_rst_total

    agent_dict_total["unanswered"] = unanswered_rst_total
    total_calls_sum = agt_report_total.count()
    agent_dict_total["total"] = total_calls_sum
    agent_pause_all = AgentBreak.objects.all()
    pause_time_all = datetime.timedelta(seconds=0)

    for ap in agent_pause_all:
        if not ap.time_spent is None:
            pause_time_all += ap.time_spent

    agent_dict_total["pausetime"] = str(pause_time_all).split('.', 2)[0]

    if "talktime" in agent_dict_total:
        idle_time_total = int(agent_dict_total["timesession"]) - (int(agent_dict_total["talktime"]) + int(agent_dict_total["holdtime"]))
        session_percent_total = round((float(agent_dict_total["talktime"]) / float(agent_dict_total["timesession"])) * 100,2)
        agent_dict_total["sessionpercent"] = "{} %".format(session_percent_total)
        agent_dict_total["talktime"] = time.strftime('%H:%M:%S', time.gmtime(agent_dict_total["talktime"]))
        agent_dict_total["holdtime"] = time.strftime('%H:%M:%S', time.gmtime(agent_dict_total["holdtime"]))
        agent_dict_total["timesession"] = time.strftime('%H:%M:%S', time.gmtime(agent_dict_total["timesession"]))
        agent_dict_total["idle_time"] = time.strftime('%H:%M:%S', time.gmtime(idle_time_total))
    agent_report_total["total"] = agent_dict_total
    context = {"agent_report": agent_report,"agent_report_total":agent_report_total,"agent_break":agent_break,
               "agent_number":agent_number,"start_date":start_date,"end_date":end_date}
    return render(request, "report/agent.html", context)

def agent_dashboard(request):
    from datetime import date
    qt = QueryTable.objects.last()
    agent_lst = []
    ext_lst = []
    agent_number = 0
    if qt is None:
        start_date = "2017-01-01 00:00:00"
        end_date = "{}-{}-{} 23:59:00".format(date.today().year, date.today().month, date.today().day)
    else:
        start_date = '{}-{}-{} {}:{}:00'.format(qt.year_from, qt.month_from, qt.day_from, qt.hour_from, qt.minute_from)
        end_date = '{}-{}-{} {}:{}:00'.format(qt.year_to, qt.month_to, qt.day_to, qt.hour_to, qt.minute_to)
        str_agent = qt.agents[1:-1]
        str_split = str_agent.split(',')
        for str_s in str_split:
            str_cl = str_s.strip()
            agent_lst.append(str_cl[1:-1])

        if agent_lst:
            agent_number = len(filter(None, agent_lst))

    if not agent_number:
        agent_number = AgentConf.objects.count()
        agenttconf = AgentConf.objects.all()
    else:
        str_ext = qt.ext[1:-1]
        str_spt = str_ext.split(',')
        for str_s in str_spt:
            str_cl = str_s.strip()
            ext_lst.append(str_cl[1:-1])
        agenttconf = AgentConf.objects.filter(extension__in=ext_lst)
    agent_dict  = dict.fromkeys(["talktime", "holdtime", "timesession","idle_time", "answered", "unanswered",
                                 "total", "pausetime","sessionpercent"],0.0000001)

    agent_report = {}
    for agents in agenttconf:
        my_agent = "Agent/{}".format(agents.extension)
        agt_report = Queue.objects.filter(agent = my_agent,time__range=(start_date, end_date))
        for row in agt_report:
            if row.event == "COMPLETECALLER" or row.event == "COMPLETEAGENT":
                if "talktime" in agent_dict:
                    agent_dict["talktime"] += int(row.data2)
            elif row.event == "CONNECT":
                if "holdtime" in agent_dict:
                    agent_dict["holdtime"] += int(row.data1)
            elif row.event == "AGENTLOGOFF":
                if "timesession" in agent_dict:
                    agent_dict["timesession"] += int(row.data2)
        answered_rst = Queue.objects.filter(
            event__in=['COMPLETECALLER', 'COMPLETEAGENT', 'TRANSFER', 'CONNECT'],agent = my_agent,time__range=(start_date, end_date)).count()
        agent_dict["answered"] = answered_rst
        unanswered_rst = Queue.objects.filter(event__in=['ABANDON', 'EXITWITHTIMEOUT'],agent = my_agent,time__range=(start_date, end_date)).count()
        agent_dict["unanswered"] = unanswered_rst
        total_calls = agt_report.count()
        agent_dict["total"] = total_calls
        agent_pause = AgentBreak.objects.filter(agent=agents.agent,time_out__range=(start_date, end_date))
        pause_time = datetime.timedelta(seconds=0)

        for ap in agent_pause:
            if not ap.time_spent is None:
                pause_time += ap.time_spent
        agent_dict["pausetime"] = pause_time

        if "talktime" in agent_dict:
            idle_time = int(agent_dict["timesession"]) - (int(agent_dict["talktime"]) + int(agent_dict["holdtime"]))
            idle_time += idle_time
            session_percent = round((float(agent_dict["talktime"])/float(agent_dict["timesession"]))*100,2)
            agent_dict["sessionpercent"] = "{} %".format(session_percent)
            agent_dict["talktime"] =  agent_dict["talktime"]
            agent_dict["holdtime"] = agent_dict["holdtime"]
            agent_dict["timesession"] = agent_dict["timesession"]
            agent_dict["idle_time"] = idle_time
        agent_name = "{} {}".format(agents.agent.first_name, agents.agent.last_name)
        agent_report[agent_name] = agent_dict
        agent_dict = dict.fromkeys(
            ["talktime", "holdtime", "timesession", "idle_time", "answered", "unanswered", "total", "pausetime",
             "sessionpercent"], 0.00000001)

    categories = []
    agent_ans = []
    agent_unans = []
    agent_talk = []
    agent_hold = []
    agent_idle = []

    for key, val in agent_report.iteritems():
        categories.append(key)
        agent_ans.append(val["answered"])
        agent_unans.append (val["unanswered"])
        if "talktime" in val:
            agent_talk.append(val["talktime"])
        else:
            agent_talk.append(0)
        if "holdtime" in val:
            agent_hold.append(val["holdtime"])
        else:
            agent_hold.append(0)
        if "idle_time" in val:
            agent_idle.append(val["idle_time"])
        else:
            agent_idle.append(0)


    context = {"agent_report": agent_report,"agent_ans":agent_ans,"agent_unans":agent_unans,
               "categories":categories,"agent_talk":agent_talk,"agent_hold":agent_hold,"agent_idle":agent_idle,
               "agent_number": agent_number, "start_date": start_date, "end_date": end_date}
    return render(request, "report/agent_dashboard.html", context)

def settings(request):
    QueryTable.objects.all().delete()
    form = SetForm(request.POST or None)
    agent_arr = []
    ext_arr = []
    if request.POST:
        date_from = form['date_from'].value()
        date_to = form['date_to'].value()
        agent = form['agents'].value()
        for agt in agent:
            agt_str = "Agent/{}".format(agt)
            ext_str = "{}".format(agt)
            agent_arr.append(agt_str)
            ext_arr.append(ext_str)
        date_from_arr = date_from.split(' ')
        date_f = date_from_arr[0]
        time_f = date_from_arr[1]
        date_arr = date_f.split("-")
        year_f = date_arr[0]
        month_f = date_arr[1]
        day_f = date_arr[2]
        time_arr = time_f.split(":")
        hour_f = time_arr[0]
        minute_f = time_arr[1]

        date_to_arr = date_to.split(' ')
        date_t = date_to_arr[0]
        time_t = date_to_arr[1]
        date_arr_t = date_t.split("-")
        year_t = date_arr_t[0]
        month_t = date_arr_t[1]
        day_t = date_arr_t[2]
        time_arr_t = time_t.split(":")
        hour_f_t = time_arr_t[0]
        minute_f_t = time_arr_t[1]

        obj = QueryTable.objects.create(year_from=year_f,month_from=month_f,day_from=day_f,
                                        hour_from=hour_f,minute_from = minute_f,year_to=year_t,month_to=month_t,day_to=day_t,
                                        hour_to=hour_f_t,minute_to= minute_f_t,agents=agent_arr,ext=ext_arr)
        return HttpResponseRedirect(reverse('report:distribution'))

    context = {"form":form}
    return render(request,"report/settings.html",context)


def today_setting(request):
    from datetime import datetime, timedelta
    dat = datetime.now()
    obj = QueryTable.objects.create(year_from=dat.year,month_from=dat.month,day_from=dat.day,
                                        hour_from="00",minute_from = "00",year_to=dat.year,month_to=dat.month,day_to=dat.day,
                                        hour_to="23",minute_to= "59")
    return HttpResponseRedirect(reverse('report:distribution'))

def month_setting(request):
    from datetime import datetime, timedelta
    dat = datetime.now()
    obj = QueryTable.objects.create(year_from=dat.year, month_from=dat.month, day_from='1',
                                    hour_from="00", minute_from="00", year_to=dat.year, month_to=dat.month,
                                    day_to='31',
                                    hour_to="23", minute_to="59")
    return HttpResponseRedirect(reverse('report:distribution'))

def year_setting(request):
    from datetime import datetime, timedelta
    dat = datetime.now()
    obj = QueryTable.objects.create(year_from=dat.year, month_from='1', day_from='1',
                                    hour_from="00", minute_from="00", year_to=dat.year, month_to='12',
                                    day_to='31',
                                    hour_to="23", minute_to="59")
    return HttpResponseRedirect(reverse('report:distribution'))


def this_week_setting(request):
    from datetime import datetime, date, timedelta
    dates = date.today()
    start_week = dates - datetime.timedelta(dates.weekday())
    end_week = start_week + datetime.timedelta(7)
    obj = QueryTable.objects.create(year_from=start_week.year, month_from=start_week.month, day_from=start_week.day,
                                    hour_from="00", minute_from="00", year_to=end_week.year, month_to=end_week.month,
                                    day_to=end_week.day,
                                    hour_to="23", minute_to="59")
    return HttpResponseRedirect(reverse('report:distribution'))


def last_seven_days_setting(request):
    from datetime import datetime, date, timedelta
    dates = date.today()
    start_date = dates - datetime.timedelta(7)
    obj = QueryTable.objects.create(year_from=start_date.year, month_from=start_date.month, day_from=start_date.day,
                                    hour_from="00", minute_from="00", year_to=dates.year, month_to=dates.month,
                                    day_to=dates.day,
                                    hour_to="23", minute_to="59")
    return HttpResponseRedirect(reverse('report:distribution'))

def last_one_year_setting(request):
    from datetime import datetime,date, timedelta
    dates = date.today()
    start_date = dates - datetime.timedelta(365)
    obj = QueryTable.objects.create(year_from=start_date.year, month_from=start_date.month, day_from=start_date.day,
                                    hour_from="00", minute_from="00", year_to=dates.year, month_to=dates.month,
                                    day_to=dates.day,
                                    hour_to="23", minute_to="59")
    return HttpResponseRedirect(reverse('report:distribution'))



def recorded_calls(request):
    from django.conf import settings
    files = sorted(
        glob.iglob(settings.AUDIO_DIRS[0] + "/*.wav"), key=os.path.getctime, reverse=True)
    audios = [os.path.basename(x) for x in files]

    return render(request, "report/recorded.html", {"audios":audios})