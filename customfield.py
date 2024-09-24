from jira import JIRA

# Jira server and authentication
jira_server = 'https://insightpulse.atlassian.net'
jira_user = 'jaiyeethereal10@gmail.com'
jira_api_token = 'ATATT3xFfGF0MgJGpSo25EyTjkBZQFB8AFrxYhA_YJleG4tUUjMEEQBNYCDTA4DqTWqTj_Y0QgprRkVTW5zlvm4k1933dZDkma_HlNwjmfdhlEPbTO_luPAGgMa7YM3iqB98rVxrwhh95zlpJwPyyQ5AMs0EGO7MorBQ_VlKtpzf12byHIMuNbc=A0E2CDFA'

# Connect to Jira
try:
    jira = JIRA(server=jira_server, basic_auth=(jira_user, jira_api_token))
except Exception as e:
    print(f"Error connecting to Jira: {e}")
    exit(1)

# Get all fields in Jira
fields = jira.fields()

# Print field names and IDs
for field in fields:
    print(f"{field['name']}: {field['id']}")
