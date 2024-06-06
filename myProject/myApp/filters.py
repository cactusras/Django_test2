import django_filters
from .models import Doctor, Doc_Expertise,Expertise,Scheduling,WorkingHour,docClinicSearch

class DoctorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    clinicID = django_filters.CharFilter(field_name= 'clinicID__name',lookup_expr='icontains')
    experise = django_filters.CharFilter(method='filter_by_exp')


    
    def filter_by_exp(self, queryset, name, value):
        return queryset.filter(field_name= 'doctorID_exp__expertise__name',lookup_expr='icontains')
    
class docClinicFilter(django_filters.FilterSet):
    appointed_date = django_filters.DateFilter(method='filter_by_appointed_date')#it is a value get from http request, don't need to be added into class meta fields
    doc_name = django_filters.CharFilter(lookup_expr='icontains')
    clinic_name = django_filters.CharFilter(lookup_expr='icontains')
    clinic_address = django_filters.CharFilter(lookup_expr='icontains')
    clinic_introduction = django_filters.CharFilter(lookup_expr='icontains')
    exp_name = django_filters.CharFilter(lookup_expr='icontains')
    #other fields in the docClinic models won't be directly filtered, so we don't have to add them here
    #if other fields in the docClinic models are used in the filtering logic but not directly filtered(start_date, end_date and day_of_week in our case), 
    #we can get it in the self defined filtering method(filter_by_appointed_date) using queryset as how I have done below

    class Meta:
        model = docClinicSearch
        fields = ['doc_name', 'clinic_name', 'clinic_address', 'clinic_introduction']

    def filter_by_appointed_date(self, queryset, name, value):
        if value:
            # Convert the appointed_date to the corresponding day of the week
            day_of_week = value.isoweekday()
            working_hours_ids = WorkingHour.objects.filter(day_of_week=day_of_week).values_list('id', flat=True)
            # Filter the queryset based on the appointed_date range and day_of_week
            return queryset.filter(
                start_date__lte=value,
                end_date__gte=value,
                day_of_week=day_of_week
            )
        return queryset

  

   