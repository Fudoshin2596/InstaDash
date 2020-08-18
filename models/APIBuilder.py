import json
import datetime
import requests
from CREDENTIALS import *

# ------------------------MANAGE AND VIEW API CAllS-------------------------- #


def getCreds():
    """ Get creds required for use in the applications
    Returns:
        dictonary: credentials needed globally
    """
    creds = dict()  # dictionary to hold everything
    creds['access_token'] = AccessToken  # access token for use with all api calls
    creds['client_id'] = ClientId  # client id from facebook app IG Graph API Test
    creds['client_secret'] = ClientSecret  # client secret from facebook app
    creds['graph_version'] = 'v8.0'  # version of the api we are hitting
    creds['graph_domain'] = 'https://graph.facebook.com/'  # base domain for api calls
    creds['endpoint_base'] = creds['graph_domain'] + creds['graph_version'] + '/'  # base endpoint with domain and version
    creds['debug'] = 'no'  # debug mode for api call
    creds['page_id'] = PageId  # users page id
    creds['instagram_account_id'] = InstagramAccountId  # users instagram account id
    creds['ig_username'] = IGUsername  # ig username
    return creds


def makeApiCall(url, endpointParams, debug='no'):
    """ Request data from endpoint with params
    Args:
        url: string of the url endpoint to make request from
        endpointParams: dictionary keyed by the names of the url parameters
    Returns:
        object: data from the endpoint
    """
    data = requests.get(url, endpointParams)  # make get request

    response = dict()  # hold response info
    response['url'] = url  # url we are hitting
    response['endpoint_params'] = endpointParams  # parameters for the endpoint
    response['endpoint_params_pretty'] = json.dumps(endpointParams, indent=4)  # pretty print for cli
    response['json_data'] = json.loads(data.content)  # response data from the api
    response['json_data_pretty'] = json.dumps(response['json_data'], indent=4)  # pretty print for cli

    if (debug == 'yes'):  # display out response info
        displayApiCallData(response)  # display response

    return response  # get and return content


def displayApiCallData(response):
    """ Print out to cli response from api call """
    print("\nURL: ")  # title
    print(response['url'])  # display url hit
    print("\nEndpoint Params: ")  # title
    print(response['endpoint_params_pretty'])  # display params passed to the endpoint
    print(response['json_data_pretty'])  # make look pretty for cli
    print("\nResponse: ")  # title


def debugAccessToken(params):
    """ Get info on an access token
    API Endpoint:
        https://graph.facebook.com/debug_token?input_token={input-token}&access_token={valid-access-token}
    Returns:
        object: data from the endpoint
    """
    endpointParams = dict()  # parameter to send to the endpoint
    endpointParams['input_token'] = params['access_token']  # input token is the access token
    endpointParams['access_token'] = params['access_token']  # access token to get debug info on

    url = params['graph_domain'] + '/debug_token'  # endpoint url

    return makeApiCall(url, endpointParams, params['debug'])  # make the api call


def getLongLivedAccessToken(params):
    """ Get long lived access token
    API Endpoint:
        https://graph.facebook.com/{graph-api-version}/oauth/access_token?grant_type=fb_exchange_token&client_id={app-id}&client_secret={app-secret}&fb_exchange_token={your-access-token}
    Returns:
        object: data from the endpoint
    """
    endpointParams = dict()  # parameter to send to the endpoint
    endpointParams['grant_type'] = 'fb_exchange_token'  # tell facebook we want to exchange token
    endpointParams['client_id'] = params['client_id']  # client id from facebook app
    endpointParams['client_secret'] = params['client_secret']  # client secret from facebook app
    endpointParams['fb_exchange_token'] = params['access_token']  # access token to get exchange for a long lived token

    url = params['endpoint_base'] + 'oauth/access_token'  # endpoint url

    return makeApiCall(url, endpointParams, params['debug'])  # make the api call


def genLLAT():
    params = getCreds()
    params['debug'] = 'yes'
    response = getLongLivedAccessToken(params)
    print( "\n ---- ACCESS TOKEN INFO ----\n") # section header
    print("Access Token:")  # label
    print(response['json_data']['access_token']) # display access token

# genLLAT()
