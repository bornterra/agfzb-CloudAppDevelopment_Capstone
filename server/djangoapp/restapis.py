import requests
import json
from .models import CarMake, CarModel, CarDealer, DealerReview
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url, **kwargs):
    api_key = kwargs.get("api_key")
    try:
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            # Call get method of requests library with URL and parameters
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)

def post_request(url, json_payload, **kwargs): 
    response = requests.post(url, json=json_payload)
    return 

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["result"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], state=dealer_doc["state"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list

def get_dealer_by_id_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["result"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"][0]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], state=dealer_doc["state"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    #a= {"id":id}
    if dealerId:
        json_result = get_request(url, **{"dealerId":dealerId})
    else:
        json_result = get_request(url)
    if json_result:
        review_lists = json_result["body"]["data"]["docs"]
        for review_list in review_lists:
            review_doc = review_list
            sentiment1 = analyze_review_sentiments(review_doc["review"])
            if review_doc["purchase"]:            
                review_obj = DealerReview(dealership=review_doc["dealership"],name=review_doc["name"],purchase=review_doc["purchase"],
                                        id=review_doc["id"],review=review_doc["review"], sentiment = sentiment1,
                                        **{
                                        "purchase_date":review_doc["purchase_date"],
                                        "car_make":review_doc["car_make"],
                                        "car_model":review_doc["car_model"],
                                        "car_year":review_doc["car_year"]}
                                        )
                results.append(review_obj)
            else:
                review_obj = DealerReview(dealership=review_doc["dealership"],name=review_doc["name"],purchase=review_doc["purchase"],
                                      id=review_doc["id"],review=review_doc["review"], sentiment = sentiment1,)
                results.append(review_obj)
    return results
# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative

def analyze_review_sentiments(dealerreview):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/b8cdb209-b9c8-4a90-ad2f-7ca4640f5609"
    api_key = "IFB9SAcpPgzwOdaQK5NysyHU0TPUDgPORu-32ONrWr_q"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2022-04-07',authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    text=dealerreview
    try:
        response = natural_language_understanding.analyze( text=text,features=Features(sentiment=SentimentOptions())).get_result()
        a = response['sentiment']['document']['label']
    except:
        a = "neutral"
    
    return(a)
