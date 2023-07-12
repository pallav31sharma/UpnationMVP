from google.ads.googleads.client import GoogleAdsClient


def get_keyword_ideas(client, customer_id, language_code, location_id, keyword_text):
    keyword_plan_idea_service = client.get_service("KeywordPlanIdeaService")

    keyword_texts = [keyword_text]

    response = keyword_plan_idea_service.generate_keyword_ideas(
        customer_id=customer_id,
        language=language_code,
        geo_target_constants=[location_id],
        keyword_and_url_seed={
            'keywords': keyword_texts
        },
    )

    keyword_ideas = response.results

    for idea in keyword_ideas:
        print(f'Keyword idea text: {idea.text.value}')
        print(f'Average monthly searches: {idea.keyword_idea_metrics.avg_monthly_searches.value}\n')


# Set up Google Ads API credentials and client
client = GoogleAdsClient.load_from_storage('google-ads.yaml')
customer_id = '134-491-8194'
language_code = 'en'
location_id = 2840  # Location ID for United States
keyword_text = 'Fobily Apps'

# Call the function to retrieve keyword ideas
get_keyword_ideas(client, customer_id, language_code, location_id, keyword_text)