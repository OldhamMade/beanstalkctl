from .base_spec import BaseSpec, skipped


class BurySpec(BaseSpec):
    def setUp(self):
        self.base_setup()

    def tearDown(self):
        self.base_teardown()

    @skipped
    def it_should_bury_a_single_ready_job(self):
        pass

    @skipped
    def it_should_bury_a_job_using_an_ID(self):
        pass

    @skipped
    def it_should_bury_a_job_using_an_ID(self):
        pass

    @skipped
    def it_should_bury_all_jobs_on_a_tube(self):
        pass
