from dataclasses import dataclass


@dataclass(frozen=True)
class UrlCacheModel:
    id: int
    url: str


class UrlCache:
    def __init__(self):
        self.url_cache = {}

    def __getitem__(self, code: str) -> UrlCacheModel:
        return self.url_cache.get(code)

    def get(self, code: str) -> UrlCacheModel:
        return self.url_cache.get(code)

    def __getattr__(self, item):
        return self.url_cache.get(item)

    def __setitem__(self, code: str, url: str):
        self.url_cache[code] = url

url_cache = UrlCache()