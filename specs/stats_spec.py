from .base_spec import BaseSpec


class StatsSpec(BaseSpec):
    def setUp(self):
        self.base_setup()


    def tearDown(self):
        self.base_teardown()


    def it_should_skip_malformed_tube_names(self):
        expected = ''
        result = self.interact('stats tube foo bar')
        self.assertEqual(
            self.clean(result),
            self.clean(expected))

