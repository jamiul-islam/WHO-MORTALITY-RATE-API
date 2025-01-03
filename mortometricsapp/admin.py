from django.contrib import admin
from .models import *

''' Code written by me starts here '''
# admin code for country model


class CountryAdmin(admin.ModelAdmin):
    list_display = ("country_name", "country_code")


class MortalityRateAdmin(admin.ModelAdmin):
    list_display = ["country_data"] + \
        [f"year_{year}" for year in range(2000, 2020)]


class MaleMortalityRateAdmin(admin.ModelAdmin):
    list_display = ["country_data"] + \
        [f"year_{year}" for year in range(2000, 2020)]


class FemaleMortalityRateAdmin(admin.ModelAdmin):
    list_display = ["country_data"] + \
        [f"year_{year}" for year in range(2000, 2020)]


class SummaryOfCountryAdmin(admin.ModelAdmin):
    list_display = ("country", "lowest_mortality_year", "highest_mortality_year", "avg_overall_mortality_rate",
                    "avg_male_mortality_rate", "avg_female_mortality_rate")


# registering table
admin.site.register(Country, CountryAdmin)
admin.site.register(MortalityRate, MortalityRateAdmin)
admin.site.register(MaleMortalityRate, MaleMortalityRateAdmin)
admin.site.register(FemaleMortalityRate, FemaleMortalityRateAdmin)
admin.site.register(SummaryOfCountry, SummaryOfCountryAdmin)

''' Code written by me ends here '''
