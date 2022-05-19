import logging
from bson import ObjectId
from flask import request, make_response, jsonify
from pymongo import MongoClient
from alephvault.http_storage.flask_app import StorageApp
from alephvault.http_storage.types.method_handlers import MethodHandler, ItemMethodHandler


logging.basicConfig()


class GetUserByLogin(MethodHandler):

    def __call__(self, client: MongoClient, resource: str, method: str, db: str, collection: str, filter: dict):
        login = request.args.get("login")
        filter = {**filter, "login": login}
        document = client[db][collection].find_one(filter)
        if document:
            return make_response(jsonify(document), 200)
        else:
            return make_response(jsonify({"code": "not-found"}), 404)


PLAYERS = {
    "login": {
        "type": "string",
        "required": True,
        "empty": False
    },
    "nickname": {
        "type": "string",
        "required": True,
        "empty": False
    },
    "password": {
        "type": "string",
        "required": True,
        "empty": False
    },
    "quest": {
        "type": "list",
        "required": True,
        "minlength": 9,
        "maxlength": 9,
        "schema": {
            "type": "dict",
            "schema": {
                "cityIndex": {
                    "type": "integer",
                    "min": 0,
                    "max": 8
                },
                "questionType": {
                    "type": "string",
                    "allowed": ["cuisine", "regional", "culture"]
                }
            }
        }
    },
    "progress": {
        "type": "integer",
        "min": 0,
        "max": 9,
        "required": True
    }
}


class GGJUIOStorageApp(StorageApp):
    """
    GGJUIO application, only holding accounts:

    - players: community.players
    """

    SETTINGS = {
        "debug": True,
        "auth": {
            "db": "auth-db",
            "collection": "api-keys"
        },
        "connection": {
            "host": "localhost",
            "port": 27017,
            "user": "admin",
            "password": "p455w0rd"
        },
        "resources": {
            "players": {
                "type": "list",
                "db": "community",
                "collection": "players",
                "soft_delete": True,
                "schema": PLAYERS,
                "projection": ["login", "password", "quest", "nickname", "progress"],
                "verbs": "*",
                "indexes": {
                    "unique-login": {
                        "unique": True,
                        "fields": "login"
                    },
                    "unique-nickname": {
                        "unique": True,
                        "fields": "nickname"
                    },
                },
                "methods": {
                    "by-login": {
                        "type": "view",
                        "handler": GetUserByLogin()
                    }
                }
            },
        }
    }

    def __init__(self, import_name: str = __name__):
        super().__init__(self.SETTINGS, import_name=import_name)
        try:
            self._client["auth-db"]["api-keys"].insert_one({"api-key": "sample-abcdef"})
        except:
            pass


if __name__ == "__main__":
    app = GGJUIOStorageApp()
    app.run("0.0.0.0", 6666)
