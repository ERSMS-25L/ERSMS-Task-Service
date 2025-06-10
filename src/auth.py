from src.config import settings
import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def initialize_firebase():
    """Initialize Firebase Admin SDK with service account credentials"""
    try:
        if not firebase_admin._apps:
            # Using service account key file
            service_account_path = settings.FIREBASE_SERVICE_ACCOUNT
            logger.info(
                f"Initializing Firebase with service account: {service_account_path}"
            )
            if service_account_path:
                cred = credentials.Certificate(service_account_path)
                firebase_admin.initialize_app(cred)
                logger.info("Firebase initialized with service account file")
            else:
                # Using default credentials (for GCP deployment)
                firebase_admin.initialize_app()
                logger.info("Firebase initialized with default credentials")
        else:
            logger.info("Firebase already initialized")
    except Exception as e:
        logger.error(f"Failed to initialize Firebase: {e}")
        raise


initialize_firebase()

security = HTTPBearer()


class FirebaseUser:
    """Model for authenticated Firebase user"""

    def __init__(self, uid: str, email: Optional[str] = None):
        self.uid = uid
        self.email = email


async def verify_firebase_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> FirebaseUser:
    try:
        token = credentials.credentials

        decoded_token = auth.verify_id_token(token)

        uid = decoded_token.get("uid")
        email = decoded_token.get("email")
        email_verified = decoded_token.get("email_verified", False)

        if not uid:
            raise HTTPException(
                status_code=401, detail="Invalid token: No user ID found"
            )

        logger.info(f"Successfully authenticated user: {uid}")
        return FirebaseUser(uid=uid, email=email, email_verified=email_verified)

    except auth.InvalidIdTokenError:
        logger.warning("Invalid Firebase ID token provided")
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    except auth.ExpiredIdTokenError:
        logger.warning("Expired Firebase ID token provided")
        raise HTTPException(status_code=401, detail="Authentication token has expired")
    except auth.RevokedIdTokenError:
        logger.warning("Revoked Firebase ID token provided")
        raise HTTPException(
            status_code=401, detail="Authentication token has been revoked"
        )
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        raise HTTPException(status_code=401, detail="Authentication failed")


async def get_current_user(
    user: FirebaseUser = Depends(verify_firebase_token),
) -> FirebaseUser:
    return user
