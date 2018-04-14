import django_tables2 as tables
from extension.models import SipExtension, AgentConf
from django_tables2.utils import A

class ExtTable(tables.Table):
    name = tables.Column(verbose_name='NAME')
    extension = tables.LinkColumn('ext:ext-detail', verbose_name='EXTENSION', args=[A('pk')])

    class Meta:
        model = SipExtension
        attrs = {"class": "paleblue"}
        fields = ('id','name','extension')
        row_attrs = {
            'data-id': lambda record: record.pk
        }

class AgentTable(tables.Table):
    username = tables.Column(verbose_name='EXTENSION')
    extension_secret = tables.LinkColumn('ext:agent-detail', verbose_name='PASSWORD', args=[A('pk')])
    agent = tables.Column(verbose_name='AGENT')
    class Meta:
        model = AgentConf
        attrs = {"class": "paleblue"}
        fields = ('id','extension','extension_secret','agent')
        row_attrs = {
            'data-id': lambda record: record.pk
        }

class HoaxSettingTable(tables.Table):
    number_hoax = tables.Column(verbose_name='CALLS PER HOAX')
    placed_hoax = tables.LinkColumn('ext:hoax-edit', verbose_name='PERIOD', args=[A('pk')])
    hoax_type = tables.Column(verbose_name='HOAX TYPE')
    review_period = tables.Column(verbose_name='REVIEW PERIOD')

    class Meta:
        model = AgentConf
        attrs = {"class": "paleblue"}
        fields = ('id','number_hoax','placed_hoax','review_period','hoax_type')
        row_attrs = {
            'data-id': lambda record: record.pk
        }