"""
Aula 04 - Modelos e Implementacoes NoSQL
Lab: Operacoes basicas em um banco de dados orientado a documentos
(MongoDB), usando a API real do pymongo.

Contexto
--------
Os testes injetam uma "collection" que implementa a MESMA interface do
pymongo (via `mongomock`, uma biblioteca que simula o MongoDB em
memoria). Ou seja: o codigo que voce escreve aqui e EXATAMENTE o mesmo
que voce escreveria contra um MongoDB de verdade -- so que os testes
automaticos nao dependem de nenhum servidor rodando.

Como testar localmente antes de enviar a PR:
    pip install -r requirements.txt
    pytest -v
"""


def insert_products(collection, products):
    """Insere os produtos e retorna a quantidade inserida."""
    result = collection.insert_many(products)
    return len(result.inserted_ids)


def find_by_category(collection, category):
    """Retorna produtos da categoria ordenados por preco crescente."""
    return list(
        collection.find(
            {"category": category},
            {"_id": 0},
        ).sort("price", 1)
    )


def average_price_by_category(collection):
    """Retorna o preco medio dos produtos agrupado por categoria."""
    pipeline = [
        {"$group": {"_id": "$category", "avg_price": {"$avg": "$price"}}}
    ]
    return {
        document["_id"]: document["avg_price"]
        for document in collection.aggregate(pipeline)
    }


def increment_stock(collection, product_id, delta):
    """Atualiza atomicamente o estoque e retorna seu novo valor."""
    result = collection.update_one(
        {"product_id": product_id},
        {"$inc": {"stock": delta}},
    )
    if result.matched_count == 0:
        return None

    document = collection.find_one({"product_id": product_id}, {"stock": 1})
    return document["stock"]