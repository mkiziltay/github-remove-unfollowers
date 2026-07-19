import time
import requests

HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}


def get_headers(token):
    headers = HEADERS.copy()
    headers["Authorization"] = f"Bearer {token}"
    return headers


def find_users_per_page(base_url, time_sleep, username, token, page_number):
    url = f"{base_url}users/{username}/following?per_page=100&page={page_number}"

    response = requests.get(
        url,
        headers=get_headers(token)
    )

    if response.status_code != 200:
        print(response.status_code)
        print(response.text)
        return None

    time.sleep(int(time_sleep))

    return response.json()


def find_unfollowers(base_url, time_sleep, username, token, list_users, list_unfollows):

    if list_users is None:
        return False

    for user in list_users:

        login = user["login"]

        url = f"{base_url}users/{login}/following/{username}"

        response = requests.get(
            url,
            headers=get_headers(token)
        )

        if response.status_code == 404:
            print(f"❌ {login} not floowing you! --------------------------------")
            list_unfollows.append(login)

        elif response.status_code == 204:
            print(f"✅ {login} following you.")

        else:
            print(login)
            print(response.status_code)
            print(response.text)

        time.sleep(int(time_sleep))

    return len(list_users) == 100


def delete_user(base_url, time_sleep, username, token, list_unfollows):

    if not list_unfollows:
        print("\nNo person to unfollow...")
        return

    print(f"\n{len(list_unfollows)} person removing...\n")

    for login in list_unfollows:

        url = f"{base_url}user/following/{login}"

        response = requests.delete(
            url,
            headers=get_headers(token)
        )

        if response.status_code == 204:
            print(f"✔ Unfollow: {login}")

        else:
            print(f"✖ {login}")
            print(response.status_code)
            print(response.text)

        time.sleep(int(time_sleep))


def unfollow_back(base_url, time_sleep, username, token):

    list_unfollows = []

    page = 1

    while True:

        users = find_users_per_page(
            base_url,
            time_sleep,
            username,
            token,
            page
        )

        if not users:
            break

        has_next = find_unfollowers(
            base_url,
            time_sleep,
            username,
            token,
            users,
            list_unfollows
        )

        if has_next:
            page += 1
        else:
            break

    delete_user(
        base_url,
        time_sleep,
        username,
        token,
        list_unfollows
    )
