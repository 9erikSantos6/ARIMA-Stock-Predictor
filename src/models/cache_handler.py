import os
from diskcache import Cache
from typing import Dict, List, Union, Any

class CacheHandler:
    """ Uma classe para gerenciar o cache """
    def __init__(self) -> None:
        self._cache_dir = os.path.join('../../.cache/', 'stockpredictor')
        os.makedirs(self._cache_dir, exist_ok=True)  # Criar diretório se não existir
        self._cache = Cache(directory=self._cache_dir, size_limit=int(1024 * 1e6))

    def insert(self, data: dict) -> None:
        """Insere um dicionário de dados no cache sem expiração"""
        for k, v in data.items():
            self._cache[k] = v

    def insert_tmp(self, data: dict, s: float) -> None:
        """Insere dados temporários no cache com tempo de expiração"""
        for k, v in data.items():
            self._cache.set(k, v, expire=s)

    def get(self, keys: Union[str, List[str]]) -> Union[Any, List[Any]]:
        """Recupera um ou mais valores do cache"""
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
            return None  # Se não encontrar nenhum item, retorna None
        return itens[0] if len(itens) == 1 else itens

    def delete(self, key: Union[str, List[str]]) -> None:
        """Deleta uma ou mais chaves do cache"""
        if isinstance(key, list):
            keys = key
        else:
            keys = [key]

        for k in keys:
            if k in self._cache:
                self._cache.delete(k)

    def memoize(self, expire: float) -> None:
        """Memoize (cache) de função com expiração"""
        return self._cache.memoize(expire=expire)

    def clear(self) -> None:
        """Limpa o cache completamente"""
        self._cache.clear()

    def close(self) -> None:
        """Fecha o cache corretamente"""
        self._cache.close()

# Exemplo de uso:
# cache_handler = CacheHandler()
# cache_handler.insert({'key_model': (2, 3, 4)})
