from fuzzywuzzy import fuzz
from .base_spec import BaseSpec, skipped


class PeekSpec(BaseSpec):
    def setUp(self):
        self.base_setup()

    def tearDown(self):
        self.base_teardown()

    def it_should_peek_at_a_ready_job(self):
        jid = self.beanstalkd.put("test")
        expected = """
id: 1
  age: 0
  ttr: 120
  state: ready
  reserves: 0
  releases: 0
  timeouts: 0
  buries: 0
  kicks: 0
--body:--
test
---------"""
        result = self.interact('peek ready default')
        self.assertGreater(
            fuzz.partial_ratio(
                self.clean(result),
                self.clean(expected)),
            97)


    def it_should_peek_at_a_buried_job(self):
        jid = self.beanstalkd.put("test")
        self.interact('bury one default')
        expected = """
id: 1
  age: 0
  ttr: 120
  state: buried
  reserves: 0
  releases: 0
  timeouts: 0
  buries: 0
  kicks: 0
--body:--
test
---------"""
        result = self.interact('peek buried default')
        self.assertGreater(
            fuzz.partial_ratio(
                self.clean(result),
                self.clean(expected)),
            97)

    def it_should_peek_at_a_delayed_job(self):
        jid = self.beanstalkd.put("test", delay=300)
        expected = """
id: 1
  age: 0
  ttr: 120
  state: delayed
  reserves: 0
  releases: 0
  timeouts: 0
  buries: 0
  kicks: 0
--body:--
test
---------"""
        result = self.interact('peek delayed default')
        print result
        self.assertGreater(
            fuzz.partial_ratio(
                self.clean(result),
                self.clean(expected)),
            97)


    def it_should_peek_at_a_job_using_an_ID(self):
        jid = self.beanstalkd.put("test")
        expected = """
id: 1
  age: 0
  ttr: 120
  state: ready
  reserves: 0
  releases: 0
  timeouts: 0
  buries: 0
  kicks: 0
--body:--
test
---------"""
        result = self.interact('peek id 1')
        self.assertGreater(
            fuzz.partial_ratio(
                self.clean(result),
                self.clean(expected)),
            97)
