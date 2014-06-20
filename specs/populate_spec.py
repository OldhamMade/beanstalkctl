import random
from .base_spec import BaseSpec


class PopulateTubeSpec(BaseSpec):
    def setUp(self):
        self.base_setup()


    def tearDown(self):
        self.base_teardown()


    def it_should_populate_the_default_tube(self):
        total = random.randint(2, 20)
        expected = '?\nCreated {0} jobs:\n  {1}'.format(total, range(1, total+1))
        self.beanstalkctl.sendline('populate tube default')
        self.beanstalkctl.expect('How many jobs would you like to create?')
        self.beanstalkctl.sendline(str(total))
        self.beanstalkctl.expect_exact('beanstalkctl> ')
        result = self.get_response()
        self.assertEqual(self.clean(result),
                         self.clean(expected))


    def it_should_populate_the_named_tube(self):
        total = random.randint(2, 20)
        expected = 'Created {0} jobs:\n  {1}'.format(total, range(1, total+1))
        self.beanstalkctl.sendline('populate tube test/populate-tube')
        self.beanstalkctl.expect_exact('Do you wish to continue? y/N')
        self.beanstalkctl.sendline('y')
        self.beanstalkctl.expect_exact('How many jobs would you like to create?')
        self.beanstalkctl.sendline(str(total))
        self.beanstalkctl.expect_exact('beanstalkctl> ')
        result = self.get_response()
        self.assertEqual(self.clean(result),
                         self.clean(expected))
