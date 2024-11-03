import os, requests

# Validate JWT in user's Authorization header
# to ensure they have access to the endpoints in the application
def token(request):
    if not "Authorization" in request.headers:
        return None, ("Missing Credentials", 401)
    
    token = request.headers["Authorization"]
    
    if not token:
        return None, ("Missing Credentials", 401)
    
    # Make a post request to Auth Service
    # to validate JWT
    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/validate",
        auth={"Authorization": token}
    )
    
    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.txt, response.status_code)
    
        