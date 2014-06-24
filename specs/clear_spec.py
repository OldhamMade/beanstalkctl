from .base_spec import BaseSpec, skipped


class ClearSpec(BaseSpec):
    def setUp(self):
        self.base_setup()

    def tearDown(self):
        self.base_teardown()

    @skipped
    def it_should_clear_a_single_tube_of_all_jobs(self):
        pass

    @skipped
    def it_should_clear_all_tubes_of_all_jobs(self):
        pass
