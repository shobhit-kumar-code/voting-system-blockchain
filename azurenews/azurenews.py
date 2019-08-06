'''
    install this first:
    python -m pip install azure-cognitiveservices-search-newssearch
'''
from azure.cognitiveservices.search.newssearch import NewsSearchAPI
from msrest.authentication import CognitiveServicesCredentials
subscription_key = "3ad6790cddaa43259003034b3725acd4"


search_term = "Election India"


client = NewsSearchAPI(CognitiveServicesCredentials(subscription_key))

news_result = client.news.search(query=search_term, market="en-us", count=10)


if news_result.value:
    print("Total estimated matches value: {}".format(
            news_result.total_estimated_matches))
    print("News result count: {}".format(len(news_result.value)).encode("utf-8"))
    for first_news_result in news_result.value:        
        print("News name: {}".format(first_news_result.name).encode("utf-8"))
        print("News url: {}".format(first_news_result.url).encode("utf-8"))
        print("News description: {}".format(first_news_result.description).encode("utf-8"))
        print("Published time: {}".format(first_news_result.date_published).encode("utf-8"))
        print("News provider: {}".format(first_news_result.provider[0].name).encode("utf-8"))
        print('\n\n\n\n')
else:
    print("Didn't see any news result data..")