from flask import Flask
from flask_cors import CORS
from jose import jwt
from urllib.request import urlopen
import json
from .extensions import ma, limiter, cache
from .models import db
from .blueprints.members import members_bp
from .blueprints.mechanics import mechanics_bp
from .blueprints.service_tickets import service_tickets_bp 
from .blueprints.inventory import inventory_bp 
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Sample API"
            }
        )


@app.route("/protected", methods=["GET"])
@token_required
def protected(payload):
    return jsonify({"message": "You access a protected route!", "user": payload})


def token_required(f):
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization header is missing", None)
        if not auth:
            return jsonify({"message": "Authorization header is missing"}), 401

        #Authorization: "Bearer <token>"
        token = auth.split()[1]

        try:
            payload = verify_token(token)
        except ValueError as e:
            return jsonify({"message": str(e)}), 401

        return f(payload, *args, **kwargs)

    return decorated


def verify_token(token):
    jsonurl = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}

    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
              "kty": key['kty'],
              "kid": key['kid'],
              "use": key['use'],
              "n": key['n'],
              "e": key['e'],
            }

        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_IDENTIFIER,
                    usser=f"https://{AUTH0_DOMAIN}/"
                )
                print('PAYLOAD', payload)
                return payload
            except jwt.ExpiredSignatureError:
                raise ValueError("Token is expired.")
            except jwt.JWTClaimsError:
                raise ValueError("Incorrect claims. Check the audience ans issuer.")
            except Exception:
                raise ValueError("Unable to parse authentication token.")
        raise ValueErro("No matching RSA Key.")


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')

    CORS(app)

    AUTH0_DOMAIN = "Auth0 Domain"
    API_IDENTIFIER = "Auth- API Identifier"
    ALGORITHMS = ["RS256"]

    ma.init_app(app)
    db.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    app.register_blueprint(members_bp, url_prefix="/members")
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")
    app.register_blueprint(service_tickets_bp, url_prefix="/service_tickets")
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app
