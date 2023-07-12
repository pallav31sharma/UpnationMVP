import argparse
import sys
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
import os

# Location IDs are listed here:
# https://developers.google.com/google-ads/api/reference/data/geotargets
# and they can also be retrieved using the GeoTargetConstantService as shown
# here: https://developers.google.com/google-ads/api/docs/targeting/location-targeting
_DEFAULT_LOCATION_IDS = ["1023191"]  # location ID for New York, NY
# A language criterion ID. For example, specify 1000 for English. For more
# information on determining this value, see the below link:
# https://developers.google.com/google-ads/api/reference/data/codes-formats#expandable-7
_DEFAULT_LANGUAGE_ID = "1000"  # language ID for English


# [START generate_keyword_ideas]
def main(
        customer_id, location_ids, language_id, keyword_texts, page_url
):
    # if specifying the relative path it is not working,so using exact path,should be changed accordingly when hosted
    client = GoogleAdsClient.load_from_storage('C:/Users/pallav/PycharmProjects/upnationMVP/MVP/APIS/Google_Ads_Api/google-ads.yaml', version="v14")
    keyword_plan_idea_service = client.get_service("KeywordPlanIdeaService")
    keyword_competition_level_enum = (
        client.enums.KeywordPlanCompetitionLevelEnum
    )
    keyword_plan_network = (
        client.enums.KeywordPlanNetworkEnum.GOOGLE_SEARCH_AND_PARTNERS
    )
    location_rns = map_locations_ids_to_resource_names(client, location_ids)
    language_rn = client.get_service("GoogleAdsService").language_constant_path(
        language_id
    )

    # Either keywords or a page_url are required to generate keyword ideas
    # so this raises an error if neither are provided.
    if not (keyword_texts or page_url):
        raise ValueError(
            "At least one of keywords or page URL is required, "
            "but neither was specified."
        )

    # Only one of the fields "url_seed", "keyword_seed", or
    # "keyword_and_url_seed" can be set on the request, depending on whether
    # keywords, a page_url or both were passed to this function.
    request = client.get_type("GenerateKeywordIdeasRequest")
    request.customer_id = customer_id
    request.language = language_rn
    request.geo_target_constants = location_rns
    request.include_adult_keywords = False
    request.keyword_plan_network = keyword_plan_network

    # To generate keyword ideas with only a page_url and no keywords we need
    # to initialize a UrlSeed object with the page_url as the "url" field.
    if not keyword_texts and page_url:
        request.url_seed.url = page_url

    # To generate keyword ideas with only a list of keywords and no page_url
    # we need to initialize a KeywordSeed object and set the "keywords" field
    # to be a list of StringValue objects.
    if keyword_texts and not page_url:
        request.keyword_seed.keywords.extend(keyword_texts)

    # To generate keyword ideas using both a list of keywords and a page_url we
    # need to initialize a KeywordAndUrlSeed object, setting both the "url" and
    # "keywords" fields.
    if keyword_texts and page_url:
        request.keyword_and_url_seed.url = page_url
        request.keyword_and_url_seed.keywords.extend(keyword_texts)

    keyword_ideas = keyword_plan_idea_service.generate_keyword_ideas(
        request=request
    )

    data = []
    for idea in keyword_ideas:
        query=idea.text
        competition_value = idea.keyword_idea_metrics.competition.name
        competition_index = idea.keyword_idea_metrics.competition_index
        low_top_of_page_bid_dollars = idea.keyword_idea_metrics.low_top_of_page_bid_micros / 1000000
        high_top_of_page_bid_dollars = idea.keyword_idea_metrics.high_top_of_page_bid_micros / 1000000

        # Create a dictionary to represent a single set of data
        idea_data = {
            'query':query,
            "competition_value": competition_value,
            "competition_index": competition_index,
            "low_top_of_page_bid_dollars": low_top_of_page_bid_dollars,
            "high_top_of_page_bid_dollars": high_top_of_page_bid_dollars
        }

        data.append(idea_data)  # Add the data to the list

        # print(
        #     f'Keyword idea text "{idea.text}" has '
        #     f'"{idea.keyword_idea_metrics.avg_monthly_searches}" '
        #     f'average monthly searches and "{competition_value}" '
        #     f"competition "
        #     f'low top bid "${low_top_of_page_bid_dollars:.2f}" '
        #     f'high top bid "${high_top_of_page_bid_dollars:.2f}" '
        #     f'competition Index "{competition_index}"\n'
        # )
    # [END generate_keyword_ideas]
    for x in data:
        print(x)

    return data


def map_locations_ids_to_resource_names(client, location_ids):
    """Converts a list of location IDs to resource names.

    Args:
        client: an initialized GoogleAdsClient instance.
        location_ids: a list of location ID strings.

    Returns:
        a list of resource name strings using the given location IDs.
    """
    build_resource_name = client.get_service(
        "GeoTargetConstantService"
    ).geo_target_constant_path
    return [build_resource_name(location_id) for location_id in location_ids]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    # googleads_client = GoogleAdsClient.load_from_storage('google-ads.yaml', version="v14")

    parser = argparse.ArgumentParser(
        description="Generates keyword ideas from a list of seed keywords."
    )

    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID.",
    )
    parser.add_argument(
        "-k",
        "--keyword_texts",
        nargs="+",
        type=str,
        required=False,
        default=[],
        help="Space-delimited list of starter keywords",
    )
    # To determine the appropriate location IDs, see:
    # https://developers.google.com/google-ads/api/reference/data/geotargets
    parser.add_argument(
        "-l",
        "--location_ids",
        nargs="+",
        type=str,
        required=False,
        default=_DEFAULT_LOCATION_IDS,
        help="Space-delimited list of location criteria IDs",
    )
    # To determine the appropriate language ID, see:
    # -
    parser.add_argument(
        "-i",
        "--language_id",
        type=str,
        required=False,
        default=_DEFAULT_LANGUAGE_ID,
        help="The language criterion ID.",
    )
    # Optional: Specify a URL string related to your business to generate ideas.
    parser.add_argument(
        "-p",
        "--page_url",
        type=str,
        required=False,
        help="A URL string related to your business",
    )

    args = parser.parse_args()

    try:
        main(
            args.customer_id,
            args.location_ids,
            args.language_id,
            args.keyword_texts,
            args.page_url,
        )
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
        sys.exit(1)
