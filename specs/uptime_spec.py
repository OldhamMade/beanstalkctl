from fuzzywuzzy import fuzz
from .base_spec import BaseSpec


class UptimeSpec(BaseSpec):
    def setUp(self):
        self.base_setup()


    def tearDown(self):
        self.base_teardown()


    def it_should_print_an_uptime(self):
        expected = '''beanstalkd uptime: 0d 0m 0s'''
        result = self.interact('uptime')

        self.assertGreater(
            fuzz.partial_ratio(
                self.clean(result),
                self.clean(expected)),
            80)
