import os
from diskcache import Cache
from typing import List, Union, Any

class CacheHandler:
    """ A class to manage the cache """
    def __init__(self) -> None:
        self._cache_dir = os.path.join('../../.cache/', 'stockpredictor')
        os.makedirs(self._cache_dir, exist_ok=True)  # Create directory if it does not exist
        self._cache = Cache(directory=self._cache_dir, size_limit=int(1024 * 1e6))

    def insert(self, data: dict) -> None:
        """Inserts a data dictionary into the cache without expiration"""
        for k, v in data.items():
            self._cache[k] = v

    def insert_tmp(self, data: dict, s: float) -> None:
        """Inserts temporary data into the cache with expiration time"""
        for k, v in data.items():
            self._cache.set(k, v, expire=s)

    def get(self, keys: Union[str, List[str]]) -> Union[Any, List[Any]]:
        """Retrieves one or more values ​​from the cache"""
        itens = []

        if isinstance(keys, list):
            chave_list = keys
        else:
            chave_list = [keys]

        for k in chave_list:
            item = self._cache.get(k, default=None)
            if item is not None:
                itens.append(item)
        if len(itens) == 0:
            return None  # If no item is found, return None
        return itens[0] if len(itens) == 1 else itens

    def delete(self, key: Union[str, List[str]]) -> None:
        """Delete one or more keys from the cache"""
        if isinstance(key, list):
            keys = key
        else:
            keys = [key]

        for k in keys:
            if k in self._cache:
                self._cache.delete(k)

    def memoize(self, expire: float) -> None:
        """Function memoize (cache) with expiration"""
        return self._cache.memoize(expire=expire)

    def clear(self) -> None:
        """Clears the cache completely"""
        self._cache.clear()

    def close(self) -> None:
        """Closes the cache correctly"""
        self._cache.close()
