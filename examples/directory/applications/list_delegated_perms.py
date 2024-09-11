"""
How to grant and revoke delegated permissions for an app using Microsoft Graph.
Delegated permissions, also called scopes or OAuth2 permissions, allow an app to call an API
on behalf of a signed-in user.


https://learn.microsoft.com/en-us/graph/permissions-grant-via-msgraph?tabs=http&pivots=grant-delegated-permissions
"""

from office365.graph_client import GraphClient
from tests import (
    test_admin_principal_name,
    test_client_id,
    test_tenant,
    test_user_principal_name,
)

client = GraphClient.with_token_interactive(
    test_tenant, test_client_id, test_admin_principal_name
)


resource = client.service_principals.get_by_name("Microsoft Graph")
user = client.users.get_by_principal_name(test_user_principal_name)
result = resource.get_delegated(test_client_id, user).execute_query()

for grant in result:
    print(grant)