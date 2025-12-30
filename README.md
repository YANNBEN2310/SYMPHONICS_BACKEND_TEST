
# IoT Energy Management API

## Projet

Ce projet est une **API REST** permettant de gérer des appareils connectés IoT contrôlant la consommation de sources de chauffage.

L’API permet :

* de **recevoir et stocker** les données envoyées par les appareils,
* de **piloter** les appareils à distance (on / off),
* de **consulter un rapport agrégé** de la consommation électrique.

---

## Contexte

Les appareils connectés :

* envoient leurs données en temps réel via un endpoint HTTP,
* transmettent uniquement les paramètres modifiés,
* peuvent être contrôlés à distance via un système de messagerie.

Hypothèses principales :

* jusqu’à **2000000**,
* environ **500 messages / jour par device**,
* seuls les paramètres `instant_power` et `temp_interior` sont stockés,
* une **mise à jour horaire** est suffisante pour le reporting.

---

## Choix techniques

### Framework API

* **FastAPI**

  * validation automatique des données,
  * bonnes performances,
  * génération automatique de la documentation API.

### Stockage

* **BigQuery** en prod
  * adapté aux gros volumes,
  * performant pour les agrégations,
  * usage analytique (reporting).
* **SQLite**
  * adapté aux simulation rapides

### Messagerie

* **Google Pub/Sub**

  * communication asynchrone,
  * découplage entre l’API et les devices.

---

## Architecture du projet

```
SYMPHONICS_BACKEND_TEST/
│
├── .env                         # variables d’environnement (non versionnées)
├── .gitignore                   # fichiers ignorés par Git
├── requirements.txt             # dépendances python
│
├── app/
│   ├── __init__.py
│   ├── main.py                  # point d’entrée de l’API FastAPI
│   ├── iot_energy.db            # base SQLite (environnement local)
│
│   ├── api/                     # définition des routes HTTP
│   │   ├── __init__.py
│   │   ├── message.py           # endpoint POST /message
│   │   ├── send.py              # endpoint POST /send
│   │   ├── report.py            # endpoint GET /report
│
│   ├── configs/                 # configs de l’appli
│   │   ├── __init__.py
│   │   └── config.py            # chargement des variables env
│
│   ├── models/                  # modèles de données Pydantic
│   │   ├── __init__.py
│   │   └── models.py            # message, Property, Command,
│
│   ├── services/                # accès aux services et à la persistance
│   │   ├── __init__.py
│   │   ├── bigquery_service.py  # accès à Google BigQuery (production)
│   │   ├── sqlite_service.py    # accès à SQLite (local / tests)
│   │   ├── pubsub_service.py    # publication des messages Pub/Sub
│   │   ├── device_memory.py     # mémoire temporaire des états appareils
│   │   └── storage_factory.py   # select SQLite ou BigQuery selon l'env
│
├── scripts/
│   ├── __init__.py
│   └── init_db_sqlite.py        # script d’initialisation de la base SQLite
│
└── README.md                    # documentation du projet

```

## Description des endpoints

### POST `/message`

reçoit les messages envoyés par les appareils IoT et stocke les données pertinentes.

#### Fonctionnement

* validation du payload JSON.
* filtrage des properties.
* stockage uniquement des champs nécessaires dans BigQuery/Slqite.

#### Exemple de query

```json
{
  "bizCode": "devicePropertyMessage",
  "bizData": {
    "devId": "bfadafebb608a154206aqu",
    "productId": "ixhko1cls7lzpwsf",
    "properties": [
      {
        "code": "instant_power",
        "dpId": 1,
        "time": 1732631573782,
        "value": 2500
      }
    ]
  },
  "ts": 1732631573782
}
```

#### Réponse

```json
{
  "status": "ok",
  "inserted": 1
}
```

---

### POST `/send`


envoie un ordre d’allumage ou d’extinction à un appareil.

#### Exemple de requête

```json
{
  "device_id": "bfadafebb608a154206aqu",
  "switch": true
}
```

#### Fonctionnement

* validation des paramètres.
* publication du message sur le topic Pub/Sub `send_command`.

#### Réponse

```json
{
  "status": "command sent"
}
```

---

###  GET `/report`

retourne un rapport agrégé de la consommation électrique par jour et par tranche horaire.

#### Exemple de réponse

```json
{
  "2024-12-18": {
    "00:00": 24577,
    "01:00": 42304
  },
  "2024-12-19": {
    "00:00": 19876,
    "01:00": 38765
  }
}
```

---

## Installation et lancement du projet

### Prérequis

* Python 3.9+
* Compte Google Cloud (pour BigQuery et Pub/Sub)
* `pip`

### Installation

```bash
git clone https://github.com/YANNBEN2310/SYMPHONICS_BACKEND_TEST.git 
cd SYMPHONICS_BACKEND_TEST
pip install -r requirements.txt
```

### Lancement de l’API

```bash
uvicorn app.main:app --reload
#changer de port s'il le faut :
uvicorn app.main:app --host 127.0.0.1 --port 9000 --reload

```

L’API est accessible à l’adresse :

```
http://localhost:8000
http://localhost:9000
...
```

---

##  Documentation de l’API

FastAPI génère automatiquement une documentation interactive.

### Swagger

```
http://localhost:8000/docs
http://localhost:9000/docs
```

Permet :

* de voir tous les endpoints,
* de tester les requêtes directement depuis le navigateur,
* de consulter les schémas JSON attendus.

### ReDoc

```
http://localhost:8000/redoc
```

version plus lisible de la doc.

---

## Tests unitaires

Les tests sont simples et ciblent les fonctionnalités clés comme message send et report.

### Lancer les tests

```bash
pytest
```

Les appels à BigQuery et Pub/Sub peuvent être mockés pour permettre des tests locaux sans dépendance externe.

---

## Hypoyheses et limites

* Les services Google Cloud sont supposés configurés.

## MERCI