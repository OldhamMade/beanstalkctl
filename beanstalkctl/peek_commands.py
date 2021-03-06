from .base import BaseCommand


class PeekCommand(BaseCommand):
    def args(self):
        return self.beanstalkd.tubes()

    def run(self, line):
        args = line.split()

        if not len(args) == 3:
            self.respond('Please specify a tube')
            return False

        tube = args[-1]

        self.beanstalkd.use(tube)

        func = getattr(self.beanstalkd, 'peek_{0}'.format(self.__cmd__))
        job = func()
        self._print_job(job)


    def _print_job(self, job):
        if not job:
            self.respond('No job found')
            return False

        self.respond("""
id: {id}
  age: {age}
  ttr: {ttr}
  state: {state}
  reserves: {reserves}
  releases: {releases}
  timeouts: {timeouts}
  buries: {buries}
  kicks: {kicks}
--body:--
{body}
---------""".format(body=job.body, **job.stats()))



class PeekByIDCommand(PeekCommand):
    __cmd__ = 'id'
    __help__ = "Peek at a specific job using it's id"

    def run(self, line):
        args = line.split()

        if not len(args) == 3:
            self.respond('Please specify a tube')
            return False

        try:
            jid = int(args[-1])
        except ValueError:
            self.respond('"{0}" is not a number'.format(args[-1]))
            return

        job = self.beanstalkd.peek(jid)
        self._print_job(job)



class PeekReadyCommand(PeekCommand):
    __cmd__ = 'ready'
    __help__ = 'Peek at the next ready job on a tube'

    def args(self):
        return self.beanstalkd.tubes()



class PeekBuriedCommand(PeekCommand):
    __cmd__ = 'buried'
    __help__ = 'Peek at the next buried job on a tube'

    def args(self):
        return self.beanstalkd.tubes()



class PeekDelayedCommand(PeekCommand):
    __cmd__ = 'delayed'
    __help__ = 'Peek at the next buried job on a tube'

    def args(self):
        return self.beanstalkd.tubes()
