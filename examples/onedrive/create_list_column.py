from examples import acquire_token_by_username_password
from office365.graph_client import GraphClient
from office365.onedrive.lists.list import List
from tests import create_unique_name

client = GraphClient(acquire_token_by_username_password)
lib = client.sites.root.lists["Documents"]  # type: List

column_name = create_unique_name("TextColumn")
column = lib.columns.add_text(column_name).execute_query()
print(column.display_name)

column.delete_object().execute_query()  # cleanup