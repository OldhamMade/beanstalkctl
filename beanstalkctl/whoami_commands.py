from .base import BaseCommand



class WhoAmICommand(BaseCommand):
    __cmd__ = 'whoami'
    __help__ = 'Show the current connection details'

    def run(self, line):
        print 'Connected to {0} on port {1}'.format(self.beanstalkd_host,
                                                    self.beanstalkd_port)


