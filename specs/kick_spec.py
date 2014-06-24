from .base_spec import BaseSpec, skipped


class KickSpec(BaseSpec):
    def setUp(self):
        self.base_setup()

    def tearDown(self):
        self.base_teardown()

    @skipped
    def it_should_kick_a_single_job_on_a_tube(self):
        pass

    @skipped
    def it_should_kick_all_jobs_on_a_tube(self):
        pass

    @skipped
    def it_should_kick_all_jobs_on_the_server(self):
        pass
