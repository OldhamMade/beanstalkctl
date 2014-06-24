from .base_spec import BaseSpec, skipped


class DeleteSpec(BaseSpec):
    def setUp(self):
        self.base_setup()

    def tearDown(self):
        self.base_teardown()

    @skipped
    def it_should_delete_a_job_using_an_ID(self):
        pass
