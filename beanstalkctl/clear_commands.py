from beanstalkc import CommandFailed
from .base import BaseCommand


RUNNING = 1


class ClearCommand(BaseCommand):
    __cmd__ = 'clear'
    __help__ = 'not implemented'

    titles = ('cleared', 'all', 'remaining')

    def _get_tube_data(self):
        tubes = {}
        for tube in self.beanstalkd.tubes():
            stats = self.beanstalkd.stats_tube(tube)
            counts = {
                'buried': stats['current-jobs-buried'],
                'delayed': stats['current-jobs-delayed'],
                'ready': stats['current-jobs-ready'],
                'reserved': stats['current-jobs-reserved'],
                'urgent': stats['current-jobs-urgent'],
            }
            counts['total'] = sum(counts.values())

            if not counts['total']:
                continue

            tubes[tube] = counts

        return tubes


    def _print_result(self, result):
        self.respond("""
Cleared:
  {ready-cleared} of {ready-all} ready jobs
  {buried-cleared} of {buried-all} buried jobs
Remaining:
  {ready-remaining} ready jobs
  {buried-remaining} buried jobs
""".format(**result))


    def _delete_job(self, job):
        try:
            job.delete()
            job.stats()

        except CommandFailed:
            # stats call should raise an exception
            # if the job was *SUCCESSFULLY* deleted
            return True

        return False


    def _clear_type(self, tube, state):
        func = getattr(self.beanstalkd, 'peek_{0}'.format(state))

        self.beanstalkd.use(tube)

        pre_stats = self.beanstalkd.stats_tube(tube)

        cleared_jobs = 0

        job = func()
        while job:
            if self._delete_job(job):
                cleared_jobs += 1

            job = func()

        post_stats = self.beanstalkd.stats_tube(tube)

        return (cleared_jobs,
                pre_stats['current-jobs-{0}'.format(state)],
                post_stats['current-jobs-{0}'.format(state)],)


    def _clear_ready(self, tube):
        return self._clear_type(tube, 'ready')


    def _clear_buried(self, tube):
        return self._clear_type(tube, 'buried')



class ClearTubeCommand(ClearCommand):
    __cmd__ = 'tube'
    __help__ = 'clear a tube of all jobs'

    def args(self):
        return self.beanstalkd.tubes()

    def run(self, line):
        args = line.split()

        if not len(args) == 3:
            self.respond('Please specify a tube')
            return False

        tube = args[-1]

        if tube not in self.beanstalkd.tubes():
            self.respond('Tube {0} does not exist.'.format(tube))
            return False

        tubes = self._get_tube_data()
        total_jobs = tubes[tube]['total']

        self.respond('\nYou are about to CLEAR {0} jobs from "{1}".'.format(
            total_jobs,
            tube,
        ))

        if not self.user_wants_to_continue():
            return False

        self.respond("\nProcessing...")

        ready = dict(zip(['ready-{0}'.format(x) for x in self.titles],
                         self._clear_ready(tube)))
        buried = dict(zip(['buried-{0}'.format(x) for x in self.titles],
                          self._clear_buried(tube)))

        self._print_result(dict(ready.items() + buried.items()))



class ClearEverythingCommand(ClearCommand):
    __cmd__ = 'everything'
    __help__ = 'clear all tubes of all jobs'

    def run(self, line):
        tubes = self._get_tube_data()

        total_tubes = len(tubes)
        total_jobs = sum(v['total'] for k, v in tubes.iteritems())

        self.respond((
            '\nYou are about to CLEAR '
            '{0} jobs from ALL tubes ({1}).').format(
            total_jobs,
            total_tubes,
        ))

        if not self.user_wants_to_continue():
            return False

        self.respond("\nProcessing...")

        ready = dict((['ready-{0}'.format(x), 0] for x in self.titles))
        buried = dict((['buried-{0}'.format(x), 0] for x in self.titles))

        for tube in tubes:
            result = self._clear_ready(tube)
            for i, item in enumerate(titles):
                ready['ready-{0}'.format(item)] += result[i]

            result = self._clear_buried(tube)
            for i, item in enumerate(titles):
                buried['buried-{0}'.format(item)] += result[i]

        self._print_result(dict(ready.items() + buried.items()))
