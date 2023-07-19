from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("", home),
    path("get_keywords_list/<str:phrase>/", get_keywords_list),
    path("world_map/<str:term>/", world_map),
    path("top_conversations/<str:term>/", top_conversations),
    path("word_cloud/<str:keyword>/", word_cloud),
    path('test/', post_data),
    path('save_query/', save_query),
    path('dashboard/market_growth/', market_growth),
    path('dashboard/top_google_searches/', top_google_searches),
    path('dashboard/business_score/', business_score),
    path('dashboard/division_of_market_share/', division_of_market_share),
    path('dashboard/total_reachable_market/', total_reachable_market),
    path('discovery/chat_api/', chat_api),
    path('discovery/generate/', generate),

]
