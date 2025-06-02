import requests

def get_location(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        if response.status_code == 200:
            data = response.json()
            # You can extract city, region, country, etc.
            city = data.get("city", "")
            region = data.get("region", "")
            country = data.get("country", "")
            return f"{city}, {region}, {country}".strip(", ")
        else:
            return "Unknown"
    except Exception as e:
        print(f"Error in get_location: {e}")
        return "Unknown"
def get_ip_address(request):
    """
    Extracts the IP address from the request object.
    Handles both direct IP and forwarded headers.
    """
    if request.headers.get("X-Forwarded-For"):
        # If behind a proxy, get the first IP in the list
        return request.headers["X-Forwarded-For"].split(",")[0].strip()
    return request.remote_addr
