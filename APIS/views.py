from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.


# external imports
import spacy
import nltk
import praw
import string
from nltk.corpus import stopwords
from rake_nltk import Rake
from pytrends.request import TrendReq

# Load the spaCy English language model
nlp = spacy.load("en_core_web_sm")
nltk.download('punkt')
nltk.download('stopwords')

# reddit instance
# pallavofficial27@gmail.com
reddit = praw.Reddit(
    client_id="DySfO6Rh7G5ZSr2gufGHiA",
    client_secret="x6-dYCAad6hGS2L34LKYHaT77_5vxQ",
    user_agent="MyAPI/0.0.1",
    username="FabStyle7",
    password="pallav99sharma",
)


def get_keywords(phrase):
    # Create an instance of the Rake object
    r = Rake()

    # Extract keywords from the phrase
    r.extract_keywords_from_text(phrase)

    # Get the ranked list of keywords
    keywords = r.get_ranked_phrases()

    # Remove stopwords
    stopwords_set = set(stopwords.words('english'))
    keywords_without_stopwords = [word for word in keywords if word.lower() not in stopwords_set]
    # Print the detected keywords
    # Remove additional action words using spaCy
    doc = nlp(" ".join(keywords_without_stopwords))
    filtered_keywords = [token.text for token in doc if token.pos_ != "VERB"]
    print("Keywords:", filtered_keywords)

    return filtered_keywords


# find top subreddits based on the term
def find_related_subreddits(term):
    # Search for subreddits related to the term
    related_subreddits = []
    top_subreddits = []

    for subreddit in reddit.subreddits.search_by_name(term):
        related_subreddits.append(subreddit)

    l = []
    for subreddit in related_subreddits:
        try:
            print(subreddit.subreddit_type)
            l.append(subreddit)
        except:
            print("Not public subreddit")

    related_subreddits = l

    # Sort the subreddits based on the number of members
    sorted_subreddits = sorted(related_subreddits, key=lambda x: x.subscribers if x.subscribers is not None else 0,
                               reverse=True)

    if len(sorted_subreddits) >= 5:
        top_subreddits = sorted_subreddits[:5]
    else:
        top_subreddits = sorted_subreddits

    return top_subreddits


def home(request):
    # Process the API request
    # Generate the data for the API response
    data = {
        'message': 'Hello, API!',
        'status': 'success'
    }

    # Return the response as JSON
    return JsonResponse(data)


def get_phrase(request, phrase):
    if request.method == 'GET':
        # Process the input phrase using spaCy
        doc = nlp(phrase)

        # Filter out irrelevant noun chunks
        stopwords_english = set(stopwords.words('english'))
        relevant_pos = ['NOUN', 'PROPN']
        relevant_entities = ['ORG', 'PRODUCT']

        keywords = []
        for chunk in doc.noun_chunks:
            if (
                    chunk.root.pos_ in relevant_pos
                    or chunk.root.ent_type_ in relevant_entities
            ) and not any(
                token.text.lower() in stopwords_english for token in chunk
            ):
                keywords.append(chunk.text)

        for word in phrase.split():
            if word.lower() == 'startup' or word.lower() == 'startups':
                keywords.append(word)

        response_data = {'keywords': keywords}

        return JsonResponse(response_data)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def world_map(requests, term):
    if requests.method == 'GET':
        pytrends = TrendReq(hl='en-US', tz=360)
        timeframe = 'today 5-y'
        geo = 'US'
        pytrends.build_payload(kw_list=[term], timeframe=timeframe, geo=geo)
        # Retrieve interest by region data
        interest_by_region_df = pytrends.interest_by_region(resolution='REGION')

        # Convert each column of the dataframe to a list
        data = {
            'geo_name': interest_by_region_df.index.tolist(),
            term: interest_by_region_df[term].tolist()
        }

        # Return the JSON response
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def top_conversations(request, term):
    if request.method == "GET":
        num_posts = 5
        # Search for posts containing the search term
        search_results = reddit.subreddit('all').search(term, sort='hot', limit=num_posts)

        posts = []
        for post in search_results:
            # Create a dictionary with relevant post information
            post_data = {
                'title': post.title,
                'url': post.url,
                'text': post.selftext,
                'num_comments': post.num_comments
            }
            posts.append(post_data)

        data = {'posts': posts}

        return JsonResponse(data)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def word_cloud(request, keyword):
    if request.method == 'GET':
        subreddits = find_related_subreddits(keyword)
        trending_terms = []
        for subreddit in subreddits:
            # Retrieve the top trending terms
            for submission in subreddit.hot(limit=50):
                title_words = get_keywords(submission.title)
                trending_terms.extend(title_words)

        # Create a word frequency dictionary for trending terms
        punctuation_set = set(string.punctuation)

        # Remove punctuation words using list comprehension
        trending_terms = [word for word in trending_terms if word not in punctuation_set]
        trending_terms_freq = {}
        for term in trending_terms:
            term = term.lower()
            if term not in trending_terms_freq:
                trending_terms_freq[term] = 1
            else:
                trending_terms_freq[term] += 1

        # Sort the trending terms by frequency
        sorted_trending_terms = sorted(trending_terms_freq.items(), key=lambda x: x[1], reverse=True)

        # Extract the most used terms
        most_used_terms = [term for term, freq in sorted_trending_terms[:10]]

        # Convert the sorted list into a dictionary
        word_freq = {word: freq for word, freq in sorted_trending_terms[:10]}

        # Plot a bar chart of trending terms
        if len(sorted_trending_terms) < 10:
            return JsonResponse({'error': 'sufficient data is not available to make word cloud'})
        # Handle the case when there are not enough terms available

        data = {'word_freq': word_freq}
        return JsonResponse(data)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
