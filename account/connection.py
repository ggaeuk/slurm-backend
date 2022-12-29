from keycloak import KeycloakOpenID
from config import KEYCLOAK_SETTINGS


class ConnectToKeycloak:
    keycloak_openid = None

    def __init__(self):
        self.keycloak_openid = KeycloakOpenID(
            server_url = KEYCLOAK_SETTINGS['server_url'],
            client_id = KEYCLOAK_SETTINGS['client_id'],
            realm_name = KEYCLOAK_SETTINGS['realm_name'],
            client_secret_key = KEYCLOAK_SETTINGS['client_secret_key']
        )

