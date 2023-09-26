import requests
import json
import os
import time
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type, wait_random_exponential


class RateLimitException(Exception):
    pass


# export GITHUB_TOKEN=xxxxx
token = os.environ.get('GITHUB_TOKEN')  # use token to maximize rate limit

url = 'https://api.github.com/search/issues'


queries = []

# single request exceed 1000 results(Github API limit), separate into different time range
date_ranges = [
    ('2023-01-01', '2023-05-01'),
    ('2022-09-01', '2023-01-01'),
    ('2022-05-01', '2022-09-01'),
    ('2022-01-01', '2022-05-01'),
    ('2021-09-01', '2022-01-01'),
    ('2021-05-01', '2021-09-01'),
    ('2021-01-01', '2021-05-01'),
    ('2020-09-01', '2021-01-01'),
    ('2020-05-01', '2020-09-01'),
    ('2020-01-01', '2020-05-01')
]

query_0 = 'regex AND evil is:closed is:pr -author:app/dependabot -author:app/dependabot-preview -author:app/renovate -author:app/greenkeeper -author:greenkeeperio-bot created:>2023-05-01'
query_n = 'regex AND evil is:closed is:pr -author:app/dependabot -author:app/dependabot-preview -author:app/renovate -author:app/greenkeeper -author:greenkeeperio-bot created:<2020-01-01'

base_query = 'regex AND evil is:closed is:pr -author:app/dependabot -author:app/dependabot-preview -author:app/renovate -author:app/greenkeeper -author:greenkeeperio-bot created:'

queries.append(query_0)     # after 2023-05-01
for start_date, end_date in date_ranges:    # separate into different time range
    queries.append(f"{base_query}{start_date}..{end_date}")
queries.append(query_n)     # before 2020-01-01

cnt = 0
cnt_with_bot = 0
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github+json'
}

pr_list = []


@retry(
    stop=stop_after_attempt(10),
    wait=wait_fixed(60) + wait_random_exponential(multiplier=1, max=60),
    retry=retry_if_exception_type(RateLimitException)
)
# auto retry if rate limited
def fetch_data(url, headers, params):
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()['items'], response.links
    elif response.status_code == 403 and 'X-RateLimit-Reset' in response.headers:
        reset_time = int(response.headers['X-RateLimit-Reset'])
        sleep_duration = max(0, reset_time - int(time.time()))
        print(f"Rate limited. Sleeping for {sleep_duration} seconds.")
        raise RateLimitException("Rate limited")
    else:
        response.raise_for_status()


for query in queries:
    params = {
        'q': query,
        'per_page': 100,
        'page': 1
    }
    while True:
        try:
            pull_requests, response_links = fetch_data(url, headers, params)
            for pr in pull_requests:
                cnt_with_bot += 1
                if pr['user']['type'] != 'Bot' and (pr['user']['login'].lower().endswith('bot') == False):
                    pr_details = {
                        'title': pr['title'],
                        'url': pr['html_url'],
                        'author': pr['user']['login']
                    }
                    pr_list.append(pr_details)
                    cnt += 1

            if 'next' in response_links:
                params['page'] += 1
                time.sleep(1)
            else:
                break
        except RateLimitException:
            print("Still rate-limited. Exiting.")
            break


print("Total number of pull requests: ", cnt)
print("Total number of pull requests with bot: ", cnt_with_bot)
with open('../data/pull_requests_regex_evil.json', 'w') as f:
    json.dump(pr_list, f)
