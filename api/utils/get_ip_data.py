from bs4 import BeautifulSoup, ResultSet, Tag
import httpx
import re

from config import API_QUERY_HOST, API_QUERY_PATH


ZERO_WIDTH_RE = re.compile(r"[\u200b-\u200f\u202a-\u202e]")

def clean_text(value: str | ResultSet[Tag]) -> str:
    if isinstance(value, (ResultSet, Tag)):
        value = value.get_text()

    if not isinstance(value, str):
        return ""

    value = ZERO_WIDTH_RE.sub("", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


async def get_ip_data(ip: str = '') -> dict:
    result = {}
    url = f"{API_QUERY_HOST}{API_QUERY_PATH}{ip}"

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url)

        soup = BeautifulSoup(response.text, 'html.parser')

        ip_provider = soup.find('div', {'class': 'query-ip-location-content-info'})
        if not ip_provider:
            return result

        info_blocks = ip_provider.find_all('div')
        result['host'] = clean_text(info_blocks[0])
        result['provider'] = clean_text(info_blocks[1])

        for li in soup.find_all('li'):
            spans = li.find_all('span')
            if len(spans) >= 3:
                key = clean_text(spans[1])
                value = clean_text(spans[2])
                result[key] = value

    except Exception as err:
        print('ip q err')
        print(err)

    return result



if __name__ == '__main__':
    import asyncio
    result = asyncio.run(get_ip_data(''))
    print(result.keys())
    for k, v in result.items():

        print(f'{k}: {v}')
