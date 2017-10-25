from .forms import RaceDayScrapperForm, HorseScrapperForm
from horsing_around import PageType


def get_scrapper_forms(request):
    return {'fixture_form': RaceDayScrapperForm(initial={'page_type': PageType.Fixture.value}),
            'result_form': RaceDayScrapperForm(initial={'page_type': PageType.Result.value}),
            'horse_form': HorseScrapperForm(initial={'page_type': PageType.Horse.value})}
