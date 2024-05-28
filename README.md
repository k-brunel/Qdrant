# Qdrant Vector Store Project

## Description

Ce projet est un exemple simple et ludique démontrant comment utiliser Qdrant, un service de vector store performant et flexible, pour la gestion et la recherche de vecteurs. Il inclut des exemples de création d'un ensemble de documents artificiels, d'enregistrement de vecteurs (embeddings) dans une base de données, de recherche sémantique à partir d'un texte et de filtrage des résultats en utilisant des métadonnées.

## Prérequis

- Docker : Assurez-vous que Docker est installé sur votre machine. [Télécharger Docker](https://www.docker.com/get-started)
- Python 3.x : Installez Python si ce n'est pas déjà fait. [Télécharger Python](https://www.python.org/downloads/)

## Installation

1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/votre-utilisateur/qdrant-vector-store-project.git
   cd qdrant-vector-store-project
   ```` 

2. Démarrez le conteneur Qdrant :
   ```bash
   docker run -p 6333:6333 qdrant/qdrant
   ```` 

3. Installez les dépendances Python :
   ```bash
   pip install -r requirements.txt
   ```` 

## Utilisation

### 1. Créer des Documents Artificiels et Enregistrer des Vecteurs

Exécutez le script `create_and_store_embeddings.py` pour générer des embeddings et les enregistrer dans Qdrant :
```bash
python create_and_store_embeddings.py
```` 

### 2. Effectuer une Recherche Sémantique

Utilisez le script `search_embeddings.py` pour effectuer une recherche sémantique basée sur un texte :
```bash
python search_embeddings.py
```` 

### 3. Ajouter des Métadonnées et Filtrer les Recherches

Pour effectuer une recherche avec filtrage basé sur des métadonnées, exécutez :
```bash
python search_with_filter.py
```` 

## Structure du Projet

- `create_and_store_embeddings.py` : Script pour créer des documents artificiels, générer des embeddings et les enregistrer dans Qdrant.
- `search_embeddings.py` : Script pour effectuer une recherche sémantique à partir d'un texte.
- `search_with_filter.py` : Script pour effectuer une recherche avec filtrage basé sur des métadonnées.
- `requirements.txt` : Liste des dépendances Python nécessaires.

## Exemples de Scripts

### create_and_store_embeddings.py

```bash
import requests
import numpy as np
from sentence_transformers import SentenceTransformer

# Initialiser le modèle pour générer des embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# URL de Qdrant
qdrant_url = "http://localhost:6333"

# Créer une collection dans Qdrant
def create_collection(collection_name):
    response = requests.put(f"{qdrant_url}/collections/{collection_name}", json={
        "vectors": {
            "size": 384,  # Taille des embeddings générés par le modèle
            "distance": "Cosine"
        }
    })
    return response.json()

# Ajouter des documents avec embeddings
def add_documents(collection_name, documents):
    embeddings = model.encode([doc['text'] for doc in documents])
    points = [
        {
            "id": i,
            "vector": embedding.tolist(),
            "payload": doc
        }
        for i, (embedding, doc) in enumerate(zip(embeddings, documents))
    ]
    response = requests.put(f"{qdrant_url}/collections/{collection_name}/points?wait=true", json={
        "points": points
    })
    return response.json()

# Créer la collection
collection_name = "my_collection"
create_collection(collection_name)

# Documents artificiels
documents = [
    {"text": "Le chat est sur le tapis", "category": "animal"},
    {"text": "Le soleil brille aujourd'hui", "category": "weather"},
    {"text": "La voiture est rouge", "category": "object"},
]

# Ajouter les documents à la collection
add_documents(collection_name, documents)
```` 

### search_embeddings.py

```bash
def search(collection_name, query, top_k=3):
    query_vector = model.encode([query])[0].tolist()
    response = requests.post(f"{qdrant_url}/collections/{collection_name}/points/search", json={
        "vector": query_vector,
        "top": top_k
    })
    return response.json()

# Effectuer une recherche
query = "Le chat est heureux"
results = search(collection_name, query)
print(results)
```` 

### search_with_filter.py

```bash
def search_with_filter(collection_name, query, filter_category, top_k=3):
    query_vector = model.encode([query])[0].tolist()
    response = requests.post(f"{qdrant_url}/collections/{collection_name}/points/search", json={
        "vector": query_vector,
        "top": top_k,
        "filter": {
            "must": [
                {
                    "key": "category",
                    "match": {
                        "value": filter_category
                    }
                }
            ]
        }
    })
    return response.json()

# Effectuer une recherche avec filtre
filter_category = "animal"
results_with_filter = search_with_filter(collection_name, "Le chat dort", filter_category)
print(results_with_filter)
```` 

## Contribuer

Les contributions sont les bienvenues ! Veuillez soumettre un pull request ou ouvrir une issue pour discuter des changements que vous souhaitez apporter.

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
