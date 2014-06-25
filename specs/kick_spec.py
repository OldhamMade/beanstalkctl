from .base_spec import BaseSpec, skipped


class KickSpec(BaseSpec):
    def setUp(self):
        self.base_setup()

    def tearDown(self):
        self.base_teardown()

    def it_should_kick_a_single_job_on_a_tube(self):
        jid = self.beanstalkd.put("test")
        self.interact('bury tube default', expect='y/N\r\n')
        self.interact('y')
        job = self.beanstalkd.peek(jid)
        self.assertTrue(job.stats()['state'] == 'buried')
        self.interact('kick one default')
        job = self.beanstalkd.peek(jid)
        self.assertTrue(job.stats()['state'] == 'ready')

    def it_should_kick_all_jobs_on_a_tube(self):
        jobs = [self.beanstalkd.put("test-{0}".format(i)) for i in range(1, 10)]
        self.interact('bury tube default', expect='y/N\r\n')
        self.interact('y')
        for jid in jobs:
            job = self.beanstalkd.peek(jid)
            self.assertTrue(job.stats()['state'] == 'buried')
        self.interact('kick tube default', expect='y/N\r\n')
        self.interact('y')
        for jid in jobs:
            job = self.beanstalkd.peek(jid)
            self.assertTrue(job.stats()['state'] == 'ready')

    def it_should_kick_all_jobs_on_the_server(self):
        jobs = []
        tubes = ['tube-{0}'.format(i)
                 for i in range(1,10)]

        for tube in tubes:
            self.beanstalkd.use(tube)
            jobs += [self.beanstalkd.put("test-{0}".format(i))
                     for i in range(1, 10)]

            self.interact('bury tube {0}'.format(tube), expect='y/N\r\n')
            self.interact('y')

        for jid in jobs:
            job = self.beanstalkd.peek(jid)
            self.assertTrue(job.stats()['state'] == 'buried')

        self.interact('kick everything', expect='y/N\r\n')
        self.interact('y')

        for jid in jobs:
            job = self.beanstalkd.peek(jid)
            self.assertTrue(job.stats()['state'] == 'ready')
