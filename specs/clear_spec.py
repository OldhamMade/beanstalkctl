import random
import beanstalkc
from .base_spec import BaseSpec, skipped


class ClearSpec(BaseSpec):
    def setUp(self):
        self.base_setup()

    def tearDown(self):
        self.base_teardown()

    def it_should_clear_a_single_tube_of_all_jobs(self):
        job_count = random.randint(1, 10)
        for i in range(job_count):
            jid = self.beanstalkd.put("test: {0}".format(i))

        total_jobs = self.beanstalkd.stats_tube('default')['current-jobs-ready']

        self.assertGreater(total_jobs, 0)
        self.assertEqual(total_jobs, job_count)

        self.interact('clear tube default', expect='y/N\r\n')
        self.interact('y')

        stats = self.beanstalkd.stats_tube('default')

        self.assertEqual(int(stats['current-jobs-ready']), 0)
        self.assertEqual(int(stats['current-jobs-buried']), 0)

    def it_should_clear_all_tubes_of_all_jobs(self):
        tube_count = random.randint(1, 10)
        for tube in range(tube_count):
            self.beanstalkd.use('tube-{0}'.format(tube))
            job_count = random.randint(0, 10)
            for job in range(job_count):
                jid = self.beanstalkd.put("test: {0}".format(job))

        total_tubes = self.beanstalkd.stats()['current-tubes']

        self.assertGreater(total_tubes, 0)

        self.interact('clear everything', expect='y/N\r\n')
        self.interact('y')

        stats = self.beanstalkd.stats()

        self.assertEqual(int(stats['current-jobs-ready']), 0)
        self.assertEqual(int(stats['current-jobs-buried']), 0)
