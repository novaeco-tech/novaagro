import os
import grpc
from ecosystem_core_auth_client import AuthServiceStub, ValidateRequest

# Connect to the internal gRPC port of the Auth service
# Default to localhost for dev, override in K8s/Docker
AUTH_URL = os.environ.get("ECOSYSTEM_CORE_AUTH_GRPC_URL", "ecosystem-core-auth:9090")

def check_permission(token):
    try:
        # Create a gRPC channel
        channel = grpc.insecure_channel(AUTH_URL)
        client = AuthServiceStub(channel)
        
        # Make the fast internal call
        request = ValidateRequest(token=token)
        response = client.ValidateToken(request)
        
        return response.is_valid
    except Exception as e:
        print(f"Auth Check Failed: {e}")
        return False