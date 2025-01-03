import factory
from factory import Faker
from .models import *


# factory class for generating the random data of the country name and country code
class CountryFactory(factory.django.DjangoModelFactory):
    country_name = Faker('name')
    country_code = Faker('word')

    class Meta:  # type: ignore
        model = Country


# factory class for generating the random data of the mortality rate of the country
# year_[i] = Faker('pyfloat', left_digits=2)
class MortalityRateFactory(factory.django.DjangoModelFactory):
    country_data = factory.SubFactory(CountryFactory)

    class Meta:  # type: ignore
        model = MortalityRate

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        for year in range(2000, 2020):
            kwargs[f'year_{year}'] = Faker('pyfloat', left_digits=2).generate({})
        return super()._create(model_class, *args, **kwargs)


# factory class for generating the random data of the male mortality rate of the country
# year_[i] = Faker('pyfloat', left_digits=2)
class MaleMortalityRateFactory(factory.django.DjangoModelFactory):
    country_data = factory.SubFactory(CountryFactory)

    class Meta:  # type: ignore
        model = MaleMortalityRate

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        for year in range(2000, 2020):
            kwargs[f'year_{year}'] = Faker('pyfloat', left_digits=2).generate({})
        return super()._create(model_class, *args, **kwargs)


# factory class for generating the random data of the female mortality rate of the country
# year_[i] = Faker('pyfloat', left_digits=2)
class FemaleMortalityRateFactory(factory.django.DjangoModelFactory):
    country_data = factory.SubFactory(CountryFactory)

    class Meta:  # type: ignore
        model = FemaleMortalityRate

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        for year in range(2000, 2020):
            kwargs[f'year_{year}'] = Faker('pyfloat', left_digits=2).generate({})
        return super()._create(model_class, *args, **kwargs)


# factory class for generating the random data of the summary of the country
class SummaryOfCountryFactory(factory.django.DjangoModelFactory):
    country = factory.SubFactory(CountryFactory)
    lowest_mortality_year = Faker('random_int', min=2000, max=2019)
    highest_mortality_year = Faker('random_int', min=2000, max=2019)
    avg_overall_mortality_rate = Faker('pyfloat', left_digits=2)
    avg_male_mortality_rate = Faker('pyfloat', left_digits=2)
    avg_female_mortality_rate = Faker('pyfloat', left_digits=2)

    class Meta:  # type: ignore
        model = SummaryOfCountry
