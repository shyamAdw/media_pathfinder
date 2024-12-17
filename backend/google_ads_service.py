from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

def authenticate(authorization_code):
    """Authenticates with the Google Ads API using an authorization code."""
    try:
        googleads_client = GoogleAdsClient.load_from_storage('google-ads.yaml')
        googleads_client.oath2_client.authorize(auth_code=authorization_code)
        return googleads_client
    except Exception as e:
        print(f"An error occurred during authentication: {e}")
        return None

def fetch_data(client, customer_id, campaign_status):
    """Fetches campaign and match type data from the Google Ads API."""
    try:
        ga_service = client.get_service("GoogleAdsService")

        # GAQL query to fetch campaign data
        campaign_query = f"""
            SELECT
                campaign.id,
                campaign.name,
                campaign.status,
                campaign.advertising_channel_type,
                metrics.cost_micros
            FROM
                campaign
            WHERE
                campaign.status = '{campaign_status}'
                AND segments.date DURING LAST_30_DAYS
            """

        # Issues a search request using streaming for campaigns.
        campaign_stream = ga_service.search_stream(
            customer_id=customer_id, query=campaign_query
        )

        all_campaign_data = []
        for campaign_batch in campaign_stream:
            for campaign_row in campaign_batch.results:
                campaign = campaign_row.campaign
                metrics = campaign_row.metrics

                # GAQL query to fetch ad group and match type data
                ad_group_query = f"""
                    SELECT
                        ad_group.id,
                        ad_group.name,
                        ad_group.status,
                        metrics.cost_micros,
                        ad_group_criterion.type,
                        ad_group_criterion.keyword.match_type
                    FROM
                        ad_group_criterion
                    WHERE
                        ad_group.status IN ('ENABLED', 'PAUSED')
                        AND campaign.id = {campaign.id}
                        AND ad_group_criterion.type = 'KEYWORD'
                        AND segments.date DURING LAST_30_DAYS
                    """

                # Issues a search request using streaming for ad groups.
                ad_group_stream = ga_service.search_stream(
                    customer_id=customer_id, query=ad_group_query
                )

                for ad_group_batch in ad_group_stream:
                    for ad_group_row in ad_group_batch.results:
                        ad_group = ad_group_row.ad_group
                        ad_group_criterion = ad_group_row.ad_group_criterion
                        

                        all_campaign_data.append({
                            "campaign_id": campaign.id,
                            "campaign_name": campaign.name,
                            "campaign_type": campaign.advertising_channel_type.name,
                            "cost": metrics.cost_micros / 1000000,
                            "match_type": ad_group_criterion.keyword.match_type.name if ad_group_criterion.type == client.enums.CriterionTypeEnum.KEYWORD else "N/A"
                        })

        return all_campaign_data

    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        return []
