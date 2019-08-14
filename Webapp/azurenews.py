'''
    install this first:
    python -m pip install azure-cognitiveservices-search-newssearch
'''
from azure.cognitiveservices.search.newssearch import NewsSearchAPI
from msrest.authentication import CognitiveServicesCredentials
subscription_key = "730223159060415484ac311dbfe15bed"


class NewsSearch:
    def news(self,search_term="Indian Election"):
        #import pdb;pdb.set_trace()
        client = NewsSearchAPI(CognitiveServicesCredentials(subscription_key))

        news_result = client.news.search(query=search_term, market="en-us", count=7)
        # import pdb; pdb.set_trace()
        if news_result.value:
            print("Total estimated matches value: {}".format(
                    news_result.total_estimated_matches))
            print("News result count: {}".format(len(news_result.value)).encode("utf-8"))
            result=[]
            for first_news_result in news_result.value:        
                subresult = []
                subresult.append("{}".format(first_news_result.name))
                subresult.append("{}".format(first_news_result.url))
                result.append(subresult)

                #result.append("{}".format(first_news_result.description))
                # print("Published time: {}".format(first_news_result.date_published).encode("utf-8"))
                # print("News provider: {}".format(first_news_result.provider[0].name).encode("utf-8"))
                # print('\n\n\n\n')
            return result
        else:
            print("Didn't see any news result data..")
    def news_candidate(self,search_term="Indian Election"):
        #import pdb;pdb.set_trace()
        client = NewsSearchAPI(CognitiveServicesCredentials(subscription_key))

        news_result = client.news.search(query=search_term, market="en-us", count=6)
        # import pdb; pdb.set_trace()
        if news_result.value:
            print("Total estimated matches value: {}".format(
                    news_result.total_estimated_matches))
            print("News result count: {}".format(len(news_result.value)).encode("utf-8"))
            result=[]
            for first_news_result in news_result.value:        
                subresult = []
                a=first_news_result.name
                # subresult.append("{}".format(first_news_result.name))
                # subresult.append("{}".format(first_news_result.url))
                result.append(a)

                #result.append("{}".format(first_news_result.description))
                # print("Published time: {}".format(first_news_result.date_published).encode("utf-8"))
                # print("News provider: {}".format(first_news_result.provider[0].name).encode("utf-8"))
                # print('\n\n\n\n')
            return result
        else:
            print("Didn't see any news result data..")
# obj=NewsSearch()
# print(obj.news())