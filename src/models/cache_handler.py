
import os
from diskcache import Cache
from typing import Dict, List, Union, Any

class CacheHandler:
    """ Uma classe para genrenciar o cache """
    def __init__(self) -> None:
        self._cache_dir = os.path.join('../../.cache/', 'stockpredictor')
        self._cache = Cache(
            directory=self._cache_dir, 
            size_limit=int(1024 * 1e6)
        )

    def insert(self, data: dict) -> None:
        for k, v in data.items():
            self._cache[k] = v

    def insert_tmp(self, data: dict, s: float) -> None:
        for k, v in data.items():
            self._cache.set(k, v, expire=s)

    def get(self, keys: Union[str, List[str]]) -> Union[Any, List[Any]]:
        itens = []

        if isinstance(keys, list):
            chave_list = keys
        else:
            chave_list = [keys]

        for k in chave_list:
            item = self._cache.get(k)
            if item is not None:
                itens.append(item)

        return itens[0] if len(itens) == 1 else itens

    def delete(self, key: Union[str, List[str]]) -> None:
        if isinstance(key, list):
            keys = key
        else:
            keys = [key]

        for k in keys:
            if k in self._cache:
                self._cache.delete(k)

    def memoize(self, expire: float) -> None:
        return self._cache.memoize(expire=expire)

    def clear(self) -> None:
        self._cache.clear()

    def close(self) -> None:
        self._cache.close()

