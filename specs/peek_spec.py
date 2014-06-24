from .base_spec import BaseSpec, skipped


class PeekSpec(BaseSpec):
    def setUp(self):
        self.base_setup()

    def tearDown(self):
        self.base_teardown()

    @skipped
    def it_should_peek_at_a_ready_job(self):
        pass

    @skipped
    def it_should_peek_at_a_buried_job(self):
        pass

    @skipped
    def it_should_peek_at_a_delayed_job(self):
        pass

    @skipped
    def it_should_peek_at_a_job_using_an_ID(self):
        pass
