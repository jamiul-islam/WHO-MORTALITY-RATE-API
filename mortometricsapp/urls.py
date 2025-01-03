from django.urls import path
from . import views
from . import api

urlpatterns = [
    # Root path serves the index function
    path('', views.index, name='index'),

    # API endpoints for mortality rate data
    path('api/countries', api.CountryList.as_view(), name='countries_list'),
    path('api/country/<str:country_code>/', api.MortalityRateList.as_view(),name='overall_mortality_rates'),
    path('api/country/<str:country_code>/male', api.MaleMortalityRateList.as_view(), name='male_mortality_rates'),
    path('api/country/<str:country_code>/female', api.FemaleMortalityRateList.as_view(), name='female_mortality_rates'),
    path('api/mortality_rate/<int:year>', api.YearlyMortalityRateList.as_view(), name='mortality_rates_of_year'),
    path('api/mortality_rate/<str:country_code>/<str:year>', api.MortalityRateByCountryAndYear.as_view(), name='avg_mortality_rates_of_country'),
    path('api/country_summary', api.SummaryOfCountryList.as_view(), name='country_summary_list')
]
