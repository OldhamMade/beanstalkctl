import random
import beanstalkc
from .base_spec import BaseSpec, skipped


class BurySpec(BaseSpec):
    def setUp(self):
        self.base_setup()

    def tearDown(self):
        self.base_teardown()

    def it_should_bury_a_single_ready_job(self):
        jid = self.beanstalkd.put("test")
        self.interact('bury one default')
        job = self.beanstalkd.peek(jid)
        self.assertTrue(job.stats()['state'] == 'buried')

    def it_should_bury_all_jobs_on_a_tube(self):
        job_count = random.randint(0, 10)
        for i in range(job_count):
            jid = self.beanstalkd.put("test: {0}".format(i))
        self.interact('bury tube default', expect='y/N\r\n')
        self.interact('y')
        stats = self.beanstalkd.stats_tube('default')
        self.assertEqual(stats['current-jobs-buried'], job_count)
