from office365.sharepoint.fields.field_geolocation_value import FieldGeolocationValue
from office365.sharepoint.fields.field_url_value import FieldUrlValue
from tests import random_seed
from tests.sharepoint.sharepoint_case import SPTestCase

from office365.sharepoint.fields.field_creation_information import FieldCreationInformation
from office365.sharepoint.fields.field_type import FieldType
from office365.sharepoint.fields.field_lookup_value import FieldLookupValue
from office365.sharepoint.fields.field_multi_choice import FieldMultiChoice
from office365.sharepoint.fields.field_multi_choice_value import FieldMultiChoiceValue
from office365.sharepoint.fields.fieldMultiLookupValue import FieldMultiLookupValue
from office365.sharepoint.fields.field_multi_user_value import FieldMultiUserValue
from office365.sharepoint.fields.field_user_value import FieldUserValue
from office365.sharepoint.listitems.listitem import ListItem
from office365.sharepoint.lists.list import List
from office365.sharepoint.lists.list_creation_information import ListCreationInformation
from office365.sharepoint.lists.list_template_type import ListTemplateType


class TestFieldValue(SPTestCase):
    target_list = None  # type: List
    target_item = None  # type: ListItem
    target_field = None  # type: FieldMultiChoice

    @classmethod
    def setUpClass(cls):
        super(TestFieldValue, cls).setUpClass()
        cls.url_field_name = "DocumentationLink"
        cls.geo_field_name = "Place"
        cls.choice_field_name = "TaskStatuses"
        cls.user_field_name = "PrimaryApprover"
        cls.lookup_field_name = "RelatedDocuments"
        cls.target_list = cls.ensure_list(cls.client.web,
                                          ListCreationInformation(
                                              "Tasks N%s" % random_seed,
                                              None,
                                              ListTemplateType.TasksWithTimelineAndHierarchy))

    @classmethod
    def tearDownClass(cls):
        cls.target_list.delete_object().execute_query()

    def test1_get_web_available_fields(self):
        web_fields = self.client.web.available_fields.get().execute_query()
        self.assertIsNotNone(web_fields.resource_path)

    def test2_set_field_text_value(self):
        items = self.target_list.items
        create_info = {
            "Title": "Task1",
        }
        self.__class__.target_item = self.target_list.add_item(create_info).execute_query()
        self.client.load(items)
        self.client.execute_query()
        self.assertGreaterEqual(len(items), 1)

    def test3_create_list_lookup_field(self):
        pass

    def test4_set_field_multi_lookup_value(self):
        item_to_update = self.__class__.target_item
        lookup_id = item_to_update.properties['Id']
        multi_lookup_value = FieldMultiLookupValue()
        multi_lookup_value.add(FieldLookupValue(lookup_id))
        updated = item_to_update.set_property("Predecessors", multi_lookup_value).update().get().execute_query()
        self.assertTrue(updated.properties['Predecessors'])

    def test5_set_field_multi_user_value(self):
        current_user = self.client.web.current_user
        multi_user_value = FieldMultiUserValue()
        multi_user_value.add(FieldUserValue.from_user(current_user))
        item_to_update = self.__class__.target_item
        item_to_update.set_property("AssignedTo",  multi_user_value).update().execute_query()

    def test6_create_list_field(self):
        create_field_info = FieldCreationInformation(self.choice_field_name, FieldType.MultiChoice)
        [create_field_info.Choices.add(choice) for choice in ["Not Started", "In Progress", "Completed", "Deferred"]]
        created_field = self.target_list.fields.add(create_field_info).execute_query()
        self.assertIsInstance(created_field, FieldMultiChoice)
        self.__class__.target_field = created_field

    def test7_set_field_multi_choice_value(self):
        item_to_update = self.__class__.target_item
        multi_choice_value = FieldMultiChoiceValue(["In Progress"])
        item_to_update.set_property(self.choice_field_name, multi_choice_value)
        item_to_update.update().execute_query()

    def test8_get_lookup_field_choices(self):
        result = self.target_list.get_lookup_field_choices(self.choice_field_name)
        self.client.execute_query()
        self.assertIsNotNone(result.value)

    def test9_create_list_url_field(self):
        create_field_info = FieldCreationInformation(self.url_field_name, FieldType.URL)
        url_field = self.target_list.fields.add(create_field_info).execute_query()
        self.assertIsNotNone(url_field.resource_path)
        self.assertEqual(url_field.type_as_string, 'URL')

    def test_10_set_url_field_value(self):
        item_to_update = self.__class__.target_item
        url = "https://docs.microsoft.com/en-us/previous-versions/office/sharepoint-server/ms472498(v=office.15)"
        field_value = FieldUrlValue(url)
        updated = item_to_update.set_property(self.url_field_name, field_value).update().get().execute_query()
        self.assertIsNotNone(updated.properties.get(self.url_field_name))
        # self.assertIsInstance(updated.properties.get('DocumentationLink'), FieldUrlValue)

    def test_11_create_list_geolocation_field(self):
        create_field_info = FieldCreationInformation(self.geo_field_name, FieldType.Geolocation)
        geo_field = self.target_list.fields.add(create_field_info).execute_query()
        self.assertIsNotNone(geo_field.resource_path)
        self.assertEqual(geo_field.type_as_string, 'Geolocation')
        # self.assertIsInstance(geo_field, FieldGeolocation)

    def test_12_set_geo_field_value(self):
        item_to_update = self.__class__.target_item
        field_value = FieldGeolocationValue(59.940117, 29.8145056)
        updated = item_to_update.set_property(self.geo_field_name, field_value).update().get().execute_query()
        self.assertIsNotNone(updated.properties.get(self.geo_field_name))

    def test_13_create_list_user_field(self):
        create_field_info = FieldCreationInformation(self.user_field_name, FieldType.User)
        user_field = self.target_list.fields.add(create_field_info).execute_query()
        self.assertIsNotNone(user_field.resource_path)
        self.assertEqual(user_field.type_as_string, 'User')

    def test_14_set_user_field_value(self):
        item_to_update = self.__class__.target_item
        current_user = self.client.web.current_user
        user_value = FieldUserValue.from_user(current_user)
        updated = item_to_update.set_property(self.user_field_name, user_value).update().get().execute_query()
        self.assertIsNotNone(updated.properties.get(self.user_field_name))

    def test_15_create_list_lookup_field(self):
        lookup_list = self.client.web.default_document_library().get().execute_query()
        create_field_info = FieldCreationInformation(title=self.lookup_field_name,
                                                     lookup_list_id=lookup_list.properties['Id'],
                                                     lookup_field_name='Title',
                                                     field_type_kind=FieldType.Lookup)
        lookup_field = self.target_list.fields.add_field(create_field_info).execute_query()
        self.assertEqual(lookup_field.type_as_string, 'Lookup')

    def test_16_set_lookup_field_value(self):
        item_to_update = self.__class__.target_item
        lookup_items = self.client.web.default_document_library().get_items().execute_query()
        if len(lookup_items) > 0:
            lookup_value = FieldLookupValue(lookup_id=lookup_items[0].properties["Id"])
            updated = item_to_update.set_property(self.lookup_field_name, lookup_value).update().get().execute_query()
            self.assertIsNotNone(updated.properties.get(self.lookup_field_name))
