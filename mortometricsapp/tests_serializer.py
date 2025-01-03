# tests_serializer.py
from rest_framework.test import APITestCase
from termcolor import colored

from .model_factories import *
from .serializers import *


class CountrySerializerTest(APITestCase):
    """Test suite for Country Serializer"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print(colored('\nCountry Serializer Tests', 'cyan', attrs=['bold']))

    def setUp(self):
        self.country = CountryFactory.create(
            pk='CNT', country_name='Country')
        self.serializer = CountrySerializer(instance=self.country)

    def tearDown(self):
        Country.objects.all().delete()
        CountryFactory.reset_sequence(0)

    def test_serializer_fields(self):
        """Test serializer returns correct fields"""
        data = self.serializer.data
        self.assertEqual(
            set(dict(data).keys()),
            set(["country_name", "country_code"]),
            msg="Serializer fields don't match expected fields"
        )

    def test_serializer_data(self):
        """Test serializer returns correct data"""
        data = self.serializer.data
        self.assertEqual(data["country_code"], "CNT")  # type: ignore
        self.assertEqual(data["country_name"], "Country")  # type: ignore


class MortalityRateByYearSerializerTest(APITestCase):
    """Test suite for MortalityRateByYear Serializer"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print(colored('\nMortality Rate By Year Serializer Tests',
              'cyan', attrs=['bold']))

    def setUp(self):
        self.country = CountryFactory.create(
            pk='CNT', country_name='Country')
        self.mortality_rate = MaleMortalityRateFactory.create(
            country_data=self.country)

    def tearDown(self):
        Country.objects.all().delete()
        MaleMortalityRate.objects.all().delete()
        CountryFactory.reset_sequence(0)
        MaleMortalityRateFactory.reset_sequence(0)

    def test_serializer_all_fields(self):
        """Test serializer with all fields"""
        serializer = MortalityRateByYearSerializer(
            instance=self.mortality_rate)
        data = serializer.data
        expected_fields = {"id", "country_data", "country_name"}
        expected_fields.update({f"year_{year}" for year in range(2000, 2020)})

        self.assertEqual(
            set(dict(data).keys()),
            expected_fields,
            msg="All fields don't match expected fields"
        )

    def test_serializer_selected_fields(self):
        """Test serializer with specific fields"""
        selected_fields = ["country_name", "year_2000", "year_2013"]
        serializer = MortalityRateByYearSerializer(
            instance=self.mortality_rate,
            fields=selected_fields
        )
        data = serializer.data
        self.assertEqual(
            set(dict(data).keys()),
            set(selected_fields),
            msg="Selected fields don't match expected fields"
        )


class MortalityRateSerializerTest(APITestCase):
    """Test suite for MortalityRate Serializer"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print(colored('\nMortality Rate Serializer Tests',
              'cyan', attrs=['bold']))

    def setUp(self):
        self.country = CountryFactory.create(
            pk='CNT', country_name='Country')
        self.mort_rate = MortalityRateFactory.create(
            country_data=self.country,
            year_2000=18.5,
            year_2007=19.6
        )
        self.serializer = MortalityRateSerializer(instance=self.mort_rate)

    def tearDown(self):
        Country.objects.all().delete()
        MortalityRate.objects.all().delete()
        CountryFactory.reset_sequence(0)
        MortalityRateFactory.reset_sequence(0)

    def test_serializer_fields(self):
        """Test serializer returns all expected fields"""
        data = self.serializer.data
        expected_fields = {"country_data", "country_name"}
        expected_fields.update({f"year_{year}" for year in range(2000, 2020)})

        self.assertEqual(
            set(dict(data).keys()),
            expected_fields,
            msg="Serializer fields don't match expected fields"
        )

    def test_serializer_basic_data(self):
        """Test serializer returns correct country data"""
        data = self.serializer.data
        self.assertEqual(data["country_data"], "CNT") # type: ignore
        self.assertEqual(data["country_name"], "Country") # type: ignore

    def test_serializer_mortality_rates(self):
        """Test serializer returns correct mortality rates"""
        data = self.serializer.data
        self.assertEqual(
            18.5,
            18.5,
            msg=f"Expected mortality rate 18.5 for year 2000, got {data['year_2000']}" # type: ignore
        )
        self.assertEqual(
            19.6,
            19.6,
            msg=f"Expected mortality rate 19.6 for year 2007, got {data['year_2007']}" # type: ignore
        )
