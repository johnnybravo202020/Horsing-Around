from .forms import FixtureForm


def get_scrapper_forms(request):
    return {'fixture_form': FixtureForm(initial={'page_type': 'F'})}
