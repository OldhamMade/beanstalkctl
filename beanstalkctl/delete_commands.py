from beanstalkc import CommandFailed
from .peek_commands import PeekCommand


class DeleteCommand(PeekCommand):
    __cmd__ = 'delete'
    __help__ = 'delete a job by ID'

    def run(self, line):
        args = line.split()

        if not len(args) == 2:
            self.respond('Please specify a job ID')
            return False

        jid = args[-1]

        if not jid.isdigit():
            self.respond('ID must be a number')
            return False

        job = self.beanstalkd.peek(int(jid))

        self.respond("You are about to delete the following job...")
        self._print_job(job)
        self.respond('')

        if not self.user_wants_to_continue():
            return self.cancel()

        try:
            job.delete()
            job.stats()

        except CommandFailed:
            self.respond('Deleted job {0} successfully.'.format(jid))
            return True

        except AttributeError:
            self.respond('Job {0} not found.'.format(jid))
            return False

        self.respond('Could not delete job {0}.'.format(jid))
        return False
