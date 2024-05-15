import django_filters
from .models import Doctor, Doc_Expertise,Expertise,Scheduling,WorkingHour

class DoctorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    clinicID = django_filters.CharFilter(field_name= 'clinicID__name',lookup_expr='icontains')
    experise = django_filters.CharFilter(method='filter_by_exp')

    
    def filter_by_exp(self, queryset, name, value):
        return queryset.filter(field_name= 'doctorID_exp__expertise__name',lookup_expr='icontains')
  

   