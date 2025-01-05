# THIS CODE IS ADAPTED FROM  https://towardsdatascience.com/use-python-scripts-to-insert-csv-data-into-django-databases-72eee7c6a433

# import libraries
import os
import sys
import django
import csv

# setting the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mortometrics.settings')
django.setup()

# importing models
from mortometricsapp.models import *  # noqa

# csv file path
mortality_rate_file = os.path.join(os.path.dirname(__file__), '../../clean_datasets/mortality_rate.csv')
male_mortality_rate_file = os.path.join(os.path.dirname(__file__), '../../clean_datasets/mortality_rate_male.csv')
female_mortality_rate_file = os.path.join(os.path.dirname(__file__), '../../clean_datasets/mortality_rate_female.csv')

# deleting all the previous data from the tables
Country.objects.all().delete()
MortalityRate.objects.all().delete()
MaleMortalityRate.objects.all().delete()
FemaleMortalityRate.objects.all().delete()


# function to save data from csv
# param file: csv file path
# param model: model to save data
# param country_model: country model to save data
def save_data_from_csv(file, model, country_model):
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        header = csv_file.__next__()

        for row in csv_reader:
            country_name, country_code, indicator_name, indicator_code, *years = row

            # Check if the country instance already exists
            country_instance, created = country_model.objects.get_or_create(
                country_code=country_code,
                defaults={'country_name': country_name}
            )

            # The country instance already existed, no need to save again
            if not created:
                pass

            # The country instance was created, save it
            if model != Country:
                mortality_rate_instance_data = {
                    'country_data': country_instance}
                for i, year in enumerate(range(2000, 2020)):
                    mortality_rate_instance_data[f'year_{year}'] = float(years[i])

                # Save the mortality rate instance
                mortality_rate_instance = model(**mortality_rate_instance_data)
                mortality_rate_instance.save()


# saving data from 3 csv files
save_data_from_csv(mortality_rate_file, MortalityRate, Country)
save_data_from_csv(male_mortality_rate_file, MaleMortalityRate, Country)
save_data_from_csv(female_mortality_rate_file, FemaleMortalityRate, Country)

# show success message after saving data
print("Data populated successfully")
