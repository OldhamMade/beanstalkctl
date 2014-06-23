from .base_spec import BaseSpec


class WhoAmISpec(BaseSpec):
    def setUp(self):
        self.base_setup()

    def tearDown(self):
        self.base_teardown()


    def it_should_show_connection_details(self):
        expected = """Connected to {0} on port {1}""".format(
            self.BEANSTALKD_HOST,
            self.BEANSTALKD_PORT,
        )
        result = self.interact('whoami')
        self.assertEqual(self.clean(result),
                         self.clean(expected))
