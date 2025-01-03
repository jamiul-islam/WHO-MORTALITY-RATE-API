# This code block is the basic serializers code.
# I followed given lecture of coursera (link : https://www.coursera.org/learn/uol-cm3035-advanced-web-development/lecture/4zxub/4-205-implementing-get)
# and documentation of Django rest framework - link : https://www.django-rest-framework.org/tutorial/quickstart/
# (link : https://joel-hanson.medium.com/advanced-serializer-usage-dynamically-modifying-fields-e7c3bc28efa6
# and documentation of Django rest framework - link : https://www.django-rest-framework.org/tutorial/quickstart/

from rest_framework import serializers
from .models import *


class CountrySerializer(serializers.ModelSerializer):
    """
    Serializer for country information.
    Handles basic country data including name and country code.
    """
    class Meta:
        model = Country
        fields = ['country_name', 'country_code']

    def create(self, validated_data):
        """
        Creates a new country instance.

        Args:
            validated_data: Dictionary of validated country data

        Returns:
            Newly created Country instance
        """
        country = Country(**validated_data)
        country.save()
        return country


class BaseMortalitySerializer(serializers.ModelSerializer):
    """
    Base serializer for mortality rate data.
    Includes common functionality shared across different mortality rate types.
    """
    # Retrieve country name from the foreign key relationship
    country_name = serializers.CharField(
        source='country_data.country_name',
        read_only=True,
        help_text="Name of the country derived from country_data relation"
    )

    class Meta:
        abstract = True
        fields = ["country_data", "country_name"] + \
            [f"year_{year}" for year in range(2000, 2020)]


class MortalityRateSerializer(BaseMortalitySerializer):
    """
    Serializer for overall mortality rates.
    Includes data for all years from 2000 to 2019.
    """
    class Meta(BaseMortalitySerializer.Meta):
        model = MortalityRate


class DynamicFieldsSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional 'fields' argument that
    controls which fields should be displayed.

    Usage:
        serializer = DynamicFieldsSerializer(data, fields=['field1', 'field2'])
    """

    def __init__(self, *args, **kwargs):
        # Pop 'fields' from kwargs to customize serializer fields
        requested_fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if requested_fields is not None:
            # Remove any fields not specified in the requested_fields
            existing_fields = set(self.fields)
            fields_to_remove = existing_fields - set(requested_fields)

            # Remove unwanted fields from serializer
            for field_name in fields_to_remove:
                self.fields.pop(field_name)


class BaseYearlyMortalitySerializer(DynamicFieldsSerializer):
    """
    Base serializer for year-specific mortality data.
    Allows dynamic field selection based on requested years.
    """
    country_name = serializers.CharField(
        source='country_data.country_name',
        read_only=True,
        help_text="Name of the country derived from country_data relation"
    )

    class Meta:
        abstract = True
        fields = '__all__'


class MortalityRateByYearSerializer(BaseYearlyMortalitySerializer):
    """Serializer for overall mortality rates with year-specific data"""
    class Meta(BaseYearlyMortalitySerializer.Meta):
        model = MortalityRate


class MaleMortalityRateSerializer(BaseYearlyMortalitySerializer):
    """Serializer for male mortality rates with year-specific data"""
    class Meta(BaseYearlyMortalitySerializer.Meta):
        model = MaleMortalityRate


class FemaleMortalityRateSerializer(BaseYearlyMortalitySerializer):
    """Serializer for female mortality rates with year-specific data"""
    class Meta(BaseYearlyMortalitySerializer.Meta):
        model = FemaleMortalityRate


class SummarySerializer(serializers.ModelSerializer):
    """
    Serializer for country summary information.
    Handles the creation and serialization of country summaries.
    """
    country = CountrySerializer

    class Meta:
        model = SummaryOfCountry
        fields = '__all__'

    def create(self, validated_data):
        """
        Creates a new country summary instance.

        Args:
            validated_data: Dictionary containing validated summary data

        Returns:
            Newly created SummaryOfCountry instance
        """
        country_code = validated_data.pop("country")
        summary = SummaryOfCountry(
            **validated_data,
            country=Country.objects.get(country_code=country_code)
        )
        summary.save()
        return summary
