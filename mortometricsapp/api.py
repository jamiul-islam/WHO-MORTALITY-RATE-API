from django.http import HttpResponse
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
import json


class CountryList(generics.ListCreateAPIView):
    """
    API endpoint that allows countries to be viewed or created.
    Provides GET (list) and POST (create) functionality.
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    def perform_create(self, serializer):
        """Creates a new country entry"""
        serializer.save()


class BaseMortalityView(APIView):
    """
    Base class for handling mortality rate views.
    Provides reusable functionality for different types of mortality data.

    Args:
        data_model: The model to query (MortalityRate variants)
        data_serializer: The serializer class for the data
    """

    def __init__(self, data_model, data_serializer):
        self.data_model = data_model
        self.data_serializer = data_serializer
        super().__init__()

    def get(self, request, country_code):
        """
        Retrieves mortality rates for a specific country.

        Args:
            country_code: The unique identifier for the country

        Returns:
            Response with serialized mortality data or 404 if not found
        """
        try:
            country = Country.objects.get(pk=country_code)
            mortality_data = self.data_model.objects.filter(
                country_data=country)
            serializer = self.data_serializer(mortality_data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except self.data_model.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class MortalityRateList(BaseMortalityView):
    """Handles overall mortality rates for a country"""

    def __init__(self):
        super().__init__(MortalityRate, MortalityRateSerializer)


class MaleMortalityRateList(BaseMortalityView):
    """Handles male-specific mortality rates"""

    def __init__(self):
        super().__init__(MaleMortalityRate, MortalityRateSerializer)


class FemaleMortalityRateList(BaseMortalityView):
    """Handles female-specific mortality rates"""

    def __init__(self):
        super().__init__(FemaleMortalityRate, MortalityRateSerializer)


class YearlyMortalityRateList(APIView):
    """Retrieves mortality rates for all countries in a specific year"""

    def get(self, request, year):
        """
        Gets mortality rates for the specified year

        Args:
            year: The year to retrieve statistics for
        """
        year_field = 'year_' + str(year)
        required_fields = [year_field, 'country_name']

        try:
            mortality_data = MortalityRate.objects.all()
            serializer = MortalityRateByYearSerializer(
                mortality_data, many=True, fields=required_fields)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except MortalityRate.DoesNotExist:
            return HttpResponse(status.HTTP_404_NOT_FOUND)


class MortalityRateByCountryAndYear(APIView):
    """
    Provides combined mortality statistics for a specific country and year,
    including overall, male, and female rates
    """

    def convert_to_dict(self, data):
        """Converts OrderedDict to regular dictionary"""
        return json.loads(json.dumps(data))

    def get(self, *args, **kwargs):
        """
        Retrieves comprehensive mortality rates for a country and year

        Returns:
            Response containing combined mortality statistics
        """
        year = kwargs.get('year')
        country_code = kwargs.get('country_code')
        year_field = 'year_' + str(year)

        try:
            country = Country.objects.get(pk=country_code)

            # Retrieve all types of mortality data
            mortality_rates = MortalityRate.objects.filter(
                country_data=country)
            male_rates = MaleMortalityRate.objects.filter(country_data=country)
            female_rates = FemaleMortalityRate.objects.filter(
                country_data=country)

            # Serialize the data
            mort_serializer = MortalityRateByYearSerializer(
                mortality_rates, many=True, fields=['country_name', year_field])
            male_serializer = MaleMortalityRateSerializer(
                male_rates, many=True, fields=[year_field])
            female_serializer = FemaleMortalityRateSerializer(
                female_rates, many=True, fields=[year_field])

            # Convert to regular dictionaries
            mort_dict = self.convert_to_dict(mort_serializer.data)
            male_dict = self.convert_to_dict(male_serializer.data)
            female_dict = self.convert_to_dict(female_serializer.data)

            # Combine statistics
            combined_data = {
                "country_name": mort_dict[0]['country_name'],
                "overall_mortality_rate": mort_dict[0][year_field],
                "male_mortality_rate": male_dict[0][year_field],
                "female_mortality_rate": female_dict[0][year_field]
            }

            return Response(combined_data, status=status.HTTP_200_OK)
        except (MortalityRate.DoesNotExist, MaleMortalityRate.DoesNotExist, FemaleMortalityRate.DoesNotExist):
            return HttpResponse(status.HTTP_404_NOT_FOUND)


class SummaryOfCountryList(generics.ListCreateAPIView):
    """
    API endpoint for retrieving and creating country summaries.
    Provides a high-level overview of mortality statistics by country.
    """
    queryset = SummaryOfCountry.objects.all()
    serializer_class = SummarySerializer

    def perform_create(self, serializer):
        """Creates a new country summary"""
        return serializer.save()
