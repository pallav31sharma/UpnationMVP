from google_auth_oauthlib.flow import InstalledAppFlow

# Define the scopes for the API access
SCOPES = ['https://www.googleapis.com/auth/adwords']

def get_refresh_token():
    # Create the flow object with the necessary information
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json',  # Path to your client secret JSON file
        scopes=SCOPES
    )

    # Run the authorization flow
    flow.run_local_server(port=8080)

    # Extract and return the refresh token
    return flow.credentials.refresh_token

# Call the function to get the refresh token
refresh_token = get_refresh_token()

# Print the refresh token
print("Refresh Token:", refresh_token)