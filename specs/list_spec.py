from .base_spec import BaseSpec


class ListCleanSpec(BaseSpec):
    def setUp(self):
        self.base_setup()


    def tearDown(self):
        self.base_teardown()


    def ensure_list_all_displays_default_only(self):
        '''ensure `list all` displays default only'''
        expected = """
Tube    | Urgent | Ready | Delayed | Buried | Reserved
--------+--------+-------+---------+--------+---------
default |      0 |     0 |       0 |      0 |        0

"""
        result = self.interact('list all')
        self.assertEqual(self.clean(result),
                         self.clean(expected))


    def ensure_list_ready_responds_correctly_when_empty(self):
        '''ensure `list ready` responds correctly when empty'''
        expected = 'No tubes have ready messages'
        result = self.interact('list ready')
        self.assertEqual(self.clean(result),
                         self.clean(expected))


    def ensure_list_buried_responds_correctly_when_empty(self):
        '''ensure `list buried` responds correctly when empty'''
        expected = 'No tubes have buried messages'
        result = self.interact('list buried')
        self.assertEqual(self.clean(result),
                         self.clean(expected))


    def ensure_list_urgent_responds_correctly_when_empty(self):
        '''ensure `list urgent` responds correctly when empty'''
        expected = 'No tubes have urgent messages'
        result = self.interact('list urgent')
        self.assertEqual(self.clean(result),
                         self.clean(expected))


    def ensure_list_delayed_responds_correctly_when_empty(self):
        '''ensure `list delayed` responds correctly when empty'''
        expected = 'No tubes have delayed messages'
        result = self.interact('list delayed')
        self.assertEqual(self.clean(result),
                         self.clean(expected))


    def ensure_list_reserved_responds_correctly_when_empty(self):
        '''ensure `list reserved` responds correctly when empty'''
        expected = 'No tubes have reserved messages'
        result = self.interact('list reserved')
        self.assertEqual(self.clean(result),
                         self.clean(expected))
