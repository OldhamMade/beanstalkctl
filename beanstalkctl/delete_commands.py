from beanstalkc import CommandFailed
from .base import BaseCommand


class DeleteCommand(BaseCommand):
    __cmd__ = 'delete'
    __help__ = 'delete a job by ID'

    def run(self, line):
        args = line.split()

        if not len(args) == 2:
            print 'Please specify a job ID'
            return

        jid = args[-1]

        if not jid.isdigit():
            print 'ID must be a number'
            return

        job = self.beanstalkd.peek(int(jid))

        try:
            job.delete()
            job.stats()

        except CommandFailed:
            print 'Deleted job {0} successfully.'.format(jid)
            return

        except AttributeError:
            print 'Job {0} not found.'.format(jid)
            return

        print 'Could not delete job {0}.'.format(jid)
        return
