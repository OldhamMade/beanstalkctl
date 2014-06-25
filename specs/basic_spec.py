import beanstalkc
from .base_spec import BaseSpec

from beanstalkctl.base import BaseCommand


class BasicSpec(BaseSpec):
    def setUp(self):
        self.base_setup()
        self.conn = beanstalkc.Connection(
            host=self.beanstalkd_host,
            port=self.beanstalkd_port)

    def tearDown(self):
        self.base_teardown()

    def ensure_beanstalkd_exists(self):
        self.assertTrue(self.beanstalkd_path)

    def ensure_beanstalkd_starts(self):
        self.assertTrue(self.conn)

    def ensure_beanstalkctl_responds(self):
        result = self.interact('help')
        self.assertTrue(result.strip())

    def it_should_format_uptime_correctly(self):
        tests = {
            100: '0h 1m 40s',
            1000: '0h 16m 40s',
            10000: '2h 46m 40s',
            100000: '27h 46m 40s',
            1000000: '277h 46m 40s',
        }
        for i, expected in tests.iteritems():
            print i, BaseCommand._format_uptime(i)
            self.assertEqual(
                BaseCommand._format_uptime(i),
                expected,
            )
