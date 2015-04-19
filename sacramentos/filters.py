import django_filters
import datetime
from sacramentos.models import Agenda



# class LogEntryFilter(django_filters.FilterSet):
#     fecha = django_filters.MethodFilter(action="filter_date_end", required=True)
#     rango_fecha = django_filters.MethodFilter(action="filter_date_start", required=True)
#
#     class Meta:
#         model = Agenda
#         fields = ('user', 'action_flag', 'fechaInicial', 'fechaFinal')
#
#     @staticmethod
#     def filter_date_start(queryset, value):
#         currentdate = datetime.datetime.strptime(value, "%d/%m/%Y")
#         currentdatetime = datetime.datetime.combine(currentdate, datetime.time.min)
#         return queryset.filter(action_time__gt=currentdatetime)
