from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.models import PointStruct
from qdrant_client.models import Filter, FieldCondition, MatchValue

# Initialisation du client Qdrant avec l'URL du serveur
client = QdrantClient(url="http://localhost:6333")

# Vérifier si la collection existe déjà
collections = client.get_collections()
collection_names = [collection.name for collection in collections.collections]

# Création de la collection seulement si elle n'existe pas
if "test_collection" not in collection_names:
    client.create_collection(
        collection_name="test_collection",
        vectors_config=VectorParams(size=4, distance=Distance.DOT),
    )
else:
    print("La collection 'test_collection' existe déjà.")

# Insertion (ou mise à jour) de plusieurs points dans la collection
operation_info = client.upsert(
    collection_name="test_collection",
    wait=True,
    points=[
        # Chaque PointStruct représente un point avec un identifiant, un vecteur et un payload (données associées)
        PointStruct(id=1, vector=[0.05, 0.61, 0.76, 0.74], payload={"city": "Berlin"}),
        PointStruct(id=2, vector=[0.19, 0.81, 0.75, 0.11], payload={"city": "London"}),
        PointStruct(id=3, vector=[0.36, 0.55, 0.47, 0.94], payload={"city": "Moscow"}),
        PointStruct(id=4, vector=[0.18, 0.01, 0.85, 0.80], payload={"city": "New York"}),
        PointStruct(id=5, vector=[0.24, 0.18, 0.22, 0.44], payload={"city": "Beijing"}),
        PointStruct(id=6, vector=[0.35, 0.08, 0.11, 0.44], payload={"city": "Mumbai"}),
    ],
)

# Impression des informations de l'opération d'insertion/mise à jour
print('Informations de l opération d insertion/mise à jour :' + str(operation_info))

# Recherche de points similaires dans la collection basée sur un vecteur de requête
search_result = client.search(
    collection_name="test_collection", 
    query_vector=[0.2, 0.1, 0.9, 0.7],  # Vecteur de requête
    limit=3  # Limite du nombre de résultats à retourner
)

# Impression des résultats de recherche
print('Impression des résultats de recherche: ' + str(search_result))

# Recherche de points similaires avec un filtre basé sur le payload
search_result = client.search(
    collection_name="test_collection",
    query_vector=[0.2, 0.1, 0.9, 0.7],  # Vecteur de requête
    query_filter=Filter(
        must=[FieldCondition(key="city", match=MatchValue(value="London"))]  # Filtre pour ne retourner que les points avec "city" égal à "London"
    ),
    with_payload=True,  # Inclure les payloads dans les résultats
    limit=3,  # Limite du nombre de résultats à retourner
)

# Impression des résultats de recherche filtrés
print('Résultats de recherche filtrés: ' + str(search_result))
