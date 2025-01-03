from django.db import models


# model for storing the data of the country name and country code
class Country(models.Model):
    country_name = models.CharField(max_length=256, null=False, blank=False)
    country_code = models.CharField(
        max_length=256, null=False, blank=False, primary_key=True)

    def __str__(self):
        return self.country_code


# model for storing the data of the mortality rate of the country
class MortalityRate(models.Model):
    country_data = models.OneToOneField(Country, on_delete=models.CASCADE)

    for year in range(2000, 2020):
        locals()[f'year_{year}'] = models.FloatField()


# model for storing the male mortality rate of the country
class MaleMortalityRate(models.Model):
    country_data = models.OneToOneField(Country, on_delete=models.CASCADE)

    for year in range(2000, 2020):
        locals()[f'year_{year}'] = models.FloatField()


# model for storing the female mortality rate of the country
class FemaleMortalityRate(models.Model):
    country_data = models.OneToOneField(Country, on_delete=models.CASCADE)

    for year in range(2000, 2020):
        locals()[f'year_{year}'] = models.FloatField()


# model for storing the summary of the country
class SummaryOfCountry(models.Model):
    country = models.OneToOneField(Country, on_delete=models.CASCADE)
    lowest_mortality_year = models.IntegerField()
    highest_mortality_year = models.IntegerField()
    avg_overall_mortality_rate = models.FloatField()
    avg_male_mortality_rate = models.FloatField()
    avg_female_mortality_rate = models.FloatField()
