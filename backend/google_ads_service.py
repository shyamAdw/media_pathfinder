from google_ads import adwords
import os

def authenticate(authorization_code):
    try:
        oauth2_client = adwords.AdWordsClient.LoadFromStorage('googleads.yaml')
        oauth2_client.oauth2_client.Authorize(auth_code=authorization_code)
        return oauth2_client
    except Exception as e:
        print(f"An error occurred during authentication: {e}")
        return None

def fetch_data(client, customer_id, campaign_status):
    # Use the Google Ads API client to fetch data
    # Construct AWQL or GAQL queries based on requirements
    # Example using AWQL (replace with GAQL for Google Ads API)
    client.SetClientCustomerId(customer_id)
    campaign_service = client.GetService('CampaignService', version='v201809')

    selector = {
        'fields': ['Id', 'Name', 'Status', 'AdvertisingChannelType', 'Cost'],
        'predicates': [
            {
                'field': 'Status',
                'operator': 'EQUALS',
                'values': [campaign_status]
            }
        ],
        'dateRange': {'min': '20230101', 'max': '20231231'} # Fixed date range for MVP
    }

    campaigns = campaign_service.get(selector)['entries']

    ad_group_service = client.GetService('AdGroupService', version='v201809')
    all_campaign_data = []

    for campaign in campaigns:
        selector = {
            'fields': ['Id', 'Name', 'Status', 'CpcBid', 'Cost'],
            'predicates': [
                {
                    'field': 'CampaignId',
                    'operator': 'EQUALS',
                    'values': [campaign['id']]
                },
                {
                    'field': 'Status',
                    'operator': 'IN',
                    'values': ['ENABLED', 'PAUSED']
                }
            ],
            'dateRange': {'min': '20230101', 'max': '20231231'}
        }
        ad_groups = ad_group_service.get(selector)['entries']

        ad_group_criterion_service = client.GetService('AdGroupCriterionService', version='v201809')

        for ad_group in ad_groups:
            selector = {
                'fields': ['KeywordMatchType', 'CpcBid', 'Status', 'Cost'],
                'predicates': [
                    {
                        'field': 'AdGroupId',
                        'operator': 'EQUALS',
                        'values': [ad_group['id']]
                    },
                    {
                        'field': 'CriteriaType',
                        'operator': 'EQUALS',
                        'values': ['KEYWORD']
                    }
                ],
                'dateRange': {'min': '20230101', 'max': '20231231'}
            }

            criteria = ad_group_criterion_service.get(selector)
            if 'entries' in criteria:
                for criterion in criteria['entries']:
                    campaign_data = {
                        'campaign_id': campaign['id'],
                        'campaign_name': campaign['name'],
                        'campaign_type': campaign['advertisingChannelType'],
                        'cost': int(criterion['biddingStrategyConfiguration']['bids'][0]['bid']['microAmount']) / 1000000 if 'biddingStrategyConfiguration' in criterion and 'bids' in criterion['biddingStrategyConfiguration'] and len(criterion['biddingStrategyConfiguration']['bids']) > 0 and 'bid' in criterion['biddingStrategyConfiguration']['bids'][0] and 'microAmount' in criterion['biddingStrategyConfiguration']['bids'][0]['bid'] else 0,
                        'match_type': criterion['matchType']
                    }
                    all_campaign_data.append(campaign_data)
    return all_campaign_data