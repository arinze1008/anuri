import django_tables2 as tables
from userprofile.models import Profile
from django_tables2.utils import A

class UserTable(tables.Table):
    last_name = tables.Column(verbose_name='LAST NAME')
    user = tables.LinkColumn('profile:profile-detail', verbose_name='USER', args=[A('pk')])
    first_name = tables.Column(verbose_name='FIRST NAME')
    # user = tables.Column(verbose_name='USER')
    callgroup = tables.Column(verbose_name='GROUP')
    phone = tables.Column(verbose_name='PHONE NUMBER')
    class Meta:
        model = Profile
        attrs = {"class": "paleblue"}
        row_attrs = {
            'data-id': lambda record: record.pk
        }