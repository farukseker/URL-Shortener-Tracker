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


async def get_ip_data(ip: str = "") -> dict:
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{API_QUERY_HOST}{ip}")
            r.raise_for_status()
            data = r.json()

        if data.get("status") != "success":
            return {}

        return {
            "ip": data.get("query"),
            "country": data.get("country"),
            "countryCode": data.get("countryCode"),
            "region": data.get("regionName"),
            "city": data.get("city"),
            "lat": data.get("lat"),
            "lon": data.get("lon"),
            "isp": data.get("isp"),
            "org": data.get("org"),
            "asn": data.get("as"),
        }

    except Exception as err:
        print("ip q err:", err)
        return {}
    

if __name__ == '__main__':
    import asyncio
    result = asyncio.run(get_ip_data(''))
    print(result.keys())
    for k, v in result.items():

        print(f'{k}: {v}')
