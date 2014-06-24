import socket
from .base_spec import BaseSpec


class WhoAmISpec(BaseSpec):
    def setUp(self):
        self.base_setup()

    def tearDown(self):
        self.base_teardown()


    def it_should_show_connection_details(self):
        hostname = socket.gethostname()

        expected = """Connected to {0} on port {1}""".format(
            hostname,
            self.BEANSTALKD_PORT,
        )

        result = self.interact('whoami')

        self.assertEqual(self.clean(result),
                         self.clean(expected))
