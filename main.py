
import requests
import json
import uuid
from bs4 import BeautifulSoup
from selenium import webdriver
import db

# driver_path = '/home/evgeny/freelance/parser_tiktok/chromedriver_linux64/chromedriver'
# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# driver = webdriver.Chrome(executable_path=driver_path, options=options)

def get_movies(genre, num, offset):
    url = 'https://graphql.kinopoisk.ru/graphql/?operationName=MovieDesktopListPage'
    moviesLimit = num
    moviesOffset = offset
    payload = """
    {"operationName":"MovieDesktopListPage","variables":{"slug":"","platform":"DESKTOP","regionId":157,"withUserData":false,"supportedFilterTypes":["BOOLEAN","SINGLE_SELECT"],"filters":{"booleanFilterValues":[{"filterId":"films","value":true}],"intRangeFilterValues":[],"singleSelectFilterValues":[{"filterId":"genre","value":""" + genre +"""}],"multiSelectFilterValues":[],"realRangeFilterValues":[]},"singleSelectFiltersLimit":250,"singleSelectFiltersOffset":0,"moviesLimit":""" + moviesLimit + ""","moviesOffset":""" + moviesOffset + ""","moviesOrder":"KP_RATING_DESC","supportedItemTypes":["COMING_SOON_MOVIE_LIST_ITEM","MOVIE_LIST_ITEM","TOP_MOVIE_LIST_ITEM","POPULAR_MOVIE_LIST_ITEM","MOST_PROFITABLE_MOVIE_LIST_ITEM","MOST_EXPENSIVE_MOVIE_LIST_ITEM","BOX_OFFICE_MOVIE_LIST_ITEM","OFFLINE_AUDIENCE_MOVIE_LIST_ITEM","RECOMMENDATION_MOVIE_LIST_ITEM"]},"query":"query MovieDesktopListPage($slug: String!, $platform: WebClientPlatform!, $withUserData: Boolean!, $regionId: Int!, $supportedFilterTypes: [FilterType]!, $filters: FilterValuesInput, $singleSelectFiltersLimit: Int!, $singleSelectFiltersOffset: Int!, $moviesLimit: Int, $moviesOffset: Int, $moviesOrder: MovieListItemOrderBy, $supportedItemTypes: [MovieListItemType]) { movieListBySlug(slug: $slug, supportedFilterTypes: $supportedFilterTypes, filters: $filters) { id name description cover { avatarsUrl __typename } ...MovieListCompositeName ...MovieListAvailableFilters ...MovieList ...DescriptionLink __typename } webPage(platform: $platform) { kpMovieListPage(movieListSlug: $slug) { htmlMeta { ...OgImage __typename } footer { ...FooterConfigData __typename } featuring { ...MovieListFeaturingData __typename } __typename } __typename } } fragment MovieListCompositeName on MovieListMeta { compositeName { parts { ... on FilterReferencedMovieListNamePart { filterValue { ... on SingleSelectFilterValue { filterId __typename } __typename } name __typename } ... on StaticMovieListNamePart { name __typename } __typename } __typename } __typename } fragment MovieListAvailableFilters on MovieListMeta { availableFilters { items { ... on BooleanFilter { ...ToggleFilter __typename } ... on SingleSelectFilter { ...SingleSelectFilters __typename } __typename } __typename } __typename } fragment ToggleFilter on BooleanFilter { id enabled name { russian __typename } __typename } fragment SingleSelectFilters on SingleSelectFilter { id name { russian __typename } hint { russian __typename } values(offset: $singleSelectFiltersOffset, limit: $singleSelectFiltersLimit) { items { name { russian __typename } selectable value __typename } __typename } __typename } fragment MovieList on MovieListMeta { movies(limit: $moviesLimit, offset: $moviesOffset, orderBy: $moviesOrder, supportedItemTypes: $supportedItemTypes) { total items { movie { id title { russian original __typename } poster { avatarsUrl fallbackUrl __typename } countries { id name __typename } genres { id name __typename } cast: members(role: [ACTOR], limit: 3) { items { details person { name originalName __typename } __typename } __typename } directors: members(role: [DIRECTOR], limit: 1) { items { details person { name originalName __typename } __typename } __typename } url rating { kinopoisk { isActive count value __typename } expectation { isActive count value __typename } __typename } mainTrailer { id isEmbedded __typename } viewOption { buttonText originalButtonText promotionIcons { avatarsUrl fallbackUrl __typename } isAvailableOnline: isWatchable(filter: {anyDevice: false, anyRegion: false}) purchasabilityStatus type rightholderLogoUrlForPoster availabilityAnnounce { availabilityDate type groupPeriodType announcePromise __typename } __typename } isTicketsAvailable(regionId: $regionId) ... on Film { productionYear duration isShortFilm top250 __typename } ... on TvSeries { releaseYears { start end __typename } seriesDuration totalDuration top250 __typename } ... on MiniSeries { releaseYears { start end __typename } seriesDuration totalDuration top250 __typename } ... on TvShow { releaseYears { start end __typename } seriesDuration totalDuration top250 __typename } ... on Video {productionYear duration isShortFilm __typename } ...MovieListUserData @include(if: $withUserData) __typename } ... on TopMovieListItem { position positionDiff rate votes __typename } ... on MostProfitableMovieListItem { boxOffice { amount __typename } budget { amount __typename } ratio __typename } ... on MostExpensiveMovieListItem { budget { amount __typename } __typename } ... on OfflineAudienceMovieListItem { viewers __typename } ... on PopularMovieListItem { positionDiff __typename } ... on BoxOfficeMovieListItem { boxOffice { amount __typename } __typename } ... on RecommendationMovieListItem { __typename } ... on ComingSoonMovieListItem { releaseDate { date accuracy __typename } __typename } __typename } __typename } __typename } fragment MovieListUserData on Movie { userData { folders { id name public __typename } watchStatuses { notInterested { value __typename } watched { value __typename } __typename } voting { value votedAt __typename } __typename } __typename } fragment DescriptionLink on MovieListMeta { descriptionLink { title url __typename } __typename } fragment OgImage on HtmlMeta { openGraph { image { avatarsUrl __typename } __typename } __typename } fragment FooterConfigData on FooterConfiguration { socialNetworkLinks { icon { avatarsUrl __typename } url __typename } appMarketLinks { icon { avatarsUrl __typename } url __typename } links { title url __typename } __typename } fragment MovieListFeaturingData on MovieListFeaturing { items { title url __typename } __typename } "}"""

    headers = dict()
    with open('headers.txt', 'r') as f:
        data = f.readlines()

    for line in data:
        key, value = line.strip().split(': ')
        headers[key] = value

    resp = requests.post(url=url, data=payload, headers=headers)
    movies = json.loads(resp.text)['data']['movieListBySlug']['movies']['items']
    return movies


def get_oscar(id):
    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    full_info = requests.get(f"https://www.kinopoisk.ru/film/{id}/awards/", headers=headers)
    if not('Награды' in full_info.text):
        print('что-то не так оскар')

    return 'Оскар, ' in full_info.text


def get_about(id):
    driver_path = '/home/evgeny/freelance/parser_tiktok/chromedriver_linux64/chromedriver'
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(executable_path=driver_path, options=options)
    url = f'https://www.kinopoisk.ru/film/{id}/'
    driver.get(url)
    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, 'html.parser')
    if not('Награды' in soup.text):
        print('что-то не так о фильме')
    if soup.find('p', {'class': 'styles_paragraph__wEGPz'}):
        return soup.find('p', {'class': 'styles_paragraph__wEGPz'}).text
    return "нет описания"



if __name__ == '__main__':
    genres = ['"comedy"', '"horror"', '"thriller"', '"drama"', '"action"', '"fantasy"', '"biography"']
    index = 10
    for genre in genres:
        for offset in range(6):
            for mov in get_movies('"horror"', '50', str(offset * 50)):
                movie = mov['movie']
                id = movie['id']
                mov_id = uuid.uuid4()
                title = movie['title']['russian']
                if title is None:
                    continue

                if movie['poster']:
                    photo = movie['poster']['avatarsUrl'][2:] + '/600x900'
                else:
                    photo = "https://www.prokerala.com/movies/assets/img/no-poster-available.jpg"
                
                country = movie['countries'][0]['name']
                actors = ''
                for i, actor in enumerate(movie['cast']['items']):
                    if i == 5:
                        break
                    if actor['person']['name']:
                        actors += actor['person']['name'] + ' '
                    else:
                        actors += actor['person']['originalName'] + ' '
                
                if len(movie['directors']['items']) > 0:
                    if movie['directors']['items'][0]['person']['name']:
                        director = movie['directors']['items'][0]['person']['name']
                    else:
                        director = movie['directors']['items'][0]['person']['originalName']
                else:
                    director = 'Нет информации'
                rating = round(float(movie['rating']['kinopoisk']['value']), 2)
                year = int(movie['productionYear'])
                oscar = get_oscar(id)

                about = get_about(id)
                # about = 'о фильме'
                db.add_film(mov_id, title, index, oscar, photo, year, country, director, actors, rating, "comedy", about)
                index += 1

                print(str(id) + '----------------------')
 





