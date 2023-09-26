import requests
import json
import os
import time
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type, wait_random_exponential


def fetch_comments(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        json_response = response.json()
        if isinstance(json_response, dict):
            return json_response.get('items', []), response.links
        elif isinstance(json_response, list):
            return json_response, response.links
        else:
            print(f"Unexpected response type: {type(json_response)}")
            return [], {}
    elif response.status_code == 403 and 'X-RateLimit-Reset' in response.headers:
        reset_time = int(response.headers['X-RateLimit-Reset'])
        sleep_duration = max(0, reset_time - int(time.time()))
        print(f"Rate limited. Sleeping for {sleep_duration} seconds.")
        raise RateLimitException("Rate limited")
    else:
        response.raise_for_status()


token = os.environ.get('GITHUB_TOKEN')  # use token to maximize rate limit


headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github+json'
}
url1 = 'https://api.github.com/repos/zulip/zulip/issues/26647/comments'
url2 = 'https://api.github.com/repos/akto-api-security/akto/issues/358/comments'

with open('../data/test_test.json', 'w') as f:
    json.dump(fetch_comments(url2, headers), f)

comments, response_links_comments = fetch_comments(
    url2, headers)
comment_list = []
for comment in comments:
    comment_body = comment['body']
    comment_list.append(comment_body)
print(comment_list)
