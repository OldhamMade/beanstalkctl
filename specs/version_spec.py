from .base_spec import BaseSpec
from beanstalkctl import __version__


class VersionSpec(BaseSpec):
    def setUp(self):
        self.base_setup()

    def tearDown(self):
        self.base_teardown()


    def it_should_display_the_correct_version(self):
        expected = 'beanstalkctl version: {0}'.format(__version__)
        result = self.interact('version')
        self.assertEqual(self.clean(result),
                         self.clean(expected))
