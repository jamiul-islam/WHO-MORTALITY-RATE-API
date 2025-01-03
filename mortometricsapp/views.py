from django.shortcuts import render
from .models import Country
from .forms import SummaryOfCountryForm

# Index function promised in urls


def index(request):
    """
    View function for the index page.
    Fetches country names and year values from the database and renders the HTML view.
    """
    # Fetch country names from the database
    countries = Country.objects.all()

    # Generate year values for fetching API
    years = [year for year in range(2000, 2020)]

    # Render HTML view with the fetched data
    return render(request, 'mortometricsapp/index.html', {
        'countries': countries,
        'years': years,
        'forms': SummaryOfCountryForm()
    })
