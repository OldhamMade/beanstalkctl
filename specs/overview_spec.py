import socket
from fuzzywuzzy import fuzz
from .base_spec import BaseSpec


class OverviewSpec(BaseSpec):
    def setUp(self):
        self.base_setup()


    def tearDown(self):
        self.base_teardown()


    def it_should_print_an_overview(self):
        hostname = socket.gethostname()

        expected = '''
Hostname: {hostname}
Pid: 43632
Uptime: 0h 0m 4s
Tubes: 1

Connections: 1 (total)
  Producers: 0 (current)
    Workers: 0 (current)

Jobs:
    Urgent: 0
     Ready: 0
   Delayed: 0
  Reserved: 0
    Buried: 0

'''.format(hostname=hostname)

        result = self.interact('overview')

        self.assertGreater(
            fuzz.partial_ratio(
                self.clean(result),
                self.clean(expected)),
            95)
