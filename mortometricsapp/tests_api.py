# test.py
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from termcolor import colored

from .model_factories import *
from .serializers import *


class CountryAPITest(APITestCase):
    """Test suite for Country API endpoints"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print(colored('\nCountry API Tests', 'cyan', attrs=['bold']))

    def setUp(self):
        self.good_url = reverse('countries_list')
        self.bad_url = 'api/country_list'
        self.good_country = CountryFactory.create(
            pk='CNT', country_name='Country')
        self.bad_country = CountryFactory.create(pk=18, country_name=18.5)

    def tearDown(self):
        Country.objects.all().delete()
        CountryFactory.reset_sequence(0)

    def test_country_list_return_success(self):
        """Test GET request to valid country list endpoint returns 200"""
        response = self.client.get(self.good_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_country_list_return_404(self):
        """Test invalid country endpoint returns 404"""
        response = self.client.get(self.bad_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_url_shows_all_country_object(self):
        """Test endpoint returns all country objects"""
        CountryFactory.create_batch(10)
        response = self.client.get(self.good_url)
        self.assertEqual(len(response.json()), 12)

    def test_read_country_properties(self):
        """Test reading country name and code"""
        data = CountrySerializer(instance=self.good_country).data
        self.assertEqual(data['country_name'], 'Country')  # type: ignore
        self.assertEqual(data['country_code'], 'CNT')  # type: ignore

    def test_create_country_success(self):
        """Test successful country creation"""
        test_country = {
            'country_name': 'Test Country',
            'country_code': 'TST'
        }
        response = self.client.post(
            self.good_url, data=test_country, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_country_fail(self):
        """Test country creation with invalid data fails"""
        data = CountrySerializer(instance=self.bad_country).data
        response = self.client.post(
            self.good_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SummaryOfCountryAPITest(APITestCase):
    """Test suite for Country Summary API endpoints"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print(colored('\nCountry Summary API Tests', 'cyan', attrs=['bold']))

    def setUp(self):
        self.good_url = reverse('country_summary_list')
        self.bad_url = 'api/x90'
        self.good_country = CountryFactory.create(
            pk='CNT', country_name='Country')
        self.good_summary = SummaryOfCountryFactory.create(
            country=self.good_country,
            lowest_mortality_year=2018,
            avg_overall_mortality_rate=18.6
        )

    def tearDown(self):
        Country.objects.all().delete()
        CountryFactory.reset_sequence(0)
        SummaryOfCountry.objects.all().delete()
        SummaryOfCountryFactory.reset_sequence(0)

    def test_summary_endpoint_responses(self):
        """Test summary endpoint response codes"""
        # Test valid URL
        response = self.client.get(self.good_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test invalid URL
        response = self.client.get(self.bad_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_summary_data_retrieval(self):
        """Test summary data retrieval and count"""
        SummaryOfCountryFactory.create_batch(10)
        response = self.client.get(self.good_url)
        self.assertEqual(len(response.json()), 11)

    def test_summary_serialization(self):
        """Test summary data serialization"""
        data = SummarySerializer(instance=self.good_summary).data
        self.assertEqual(data['country'], 'CNT')  # type: ignore
        self.assertEqual(data['lowest_mortality_year'], 2018)  # type: ignore
        self.assertEqual(data['avg_overall_mortality_rate'], 18.6) # type: ignore

    def test_create_summary_validations(self):
        """Test summary creation validation rules"""
        # Test duplicate country
        data = SummarySerializer(self.good_summary).data
        response = self.client.post(
            self.good_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class YearlyMortalityRateListTest(APITestCase):
    """Test suite for Yearly Mortality Rate endpoints"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print(colored('\nYearly Mortality Rate Tests', 'cyan', attrs=['bold']))

    def setUp(self):
        self.country = CountryFactory.create(
            country_code='ABC',
            country_name='ABC country'
        )

    def test_api_url_return_success(self):
        """Test yearly mortality rate endpoint"""
        url = reverse('mortality_rates_of_year', kwargs={'year': 2000})
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
