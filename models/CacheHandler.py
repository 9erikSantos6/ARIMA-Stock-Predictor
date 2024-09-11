from diskcache import Cache

class CacheHandler:
    def __init__(self) -> None:
        self.cache = Cache(
            directory='./data/.stockpredictor_tmp_cache', 
            size_limit=int(1024 * 1e6)
        )

    def insert(self, data: dict) -> None:
        for k, v in data.items():
            self.cache[k] = v

    def insert_tmp(self, data: dict, s: float) -> None:
        for k, v in data.items():
            self.cache.set(k, v, expire=s)

    def get(self, keys):
        itens = []

        if isinstance(keys, list):
            chave_list = keys
        else:
            chave_list = [keys]

        for k in chave_list:
            item = self.cache.get(k)
            if item is not None:
                itens.append(item)

        return itens[0] if len(itens) == 1 else itens


    def memoize(self, expire: float):
        return self.cache.memoize(expire=expire)

    def close(self) -> None:
        self.cache.close()

