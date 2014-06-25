import beanstalkc
from .base_spec import BaseSpec, skipped


class DeleteSpec(BaseSpec):
    def setUp(self):
        self.base_setup()

    def tearDown(self):
        self.base_teardown()

    def it_should_delete_a_job_using_an_ID(self):
        jid = self.beanstalkd.put("test")
        self.interact('delete {0}'.format(jid), expect='y/N\r\n')
        self.interact('y')
        job = self.beanstalkd.peek(jid)
        self.assertIsNone(job)
        stats = self.beanstalkd.stats_tube('default')
        self.assertEqual(stats['current-jobs-ready'], 0)
