from ishell.command import Command
from .util import BeanstalkdMixin


class BaseCommand(Command, BeanstalkdMixin):
    def __init__(self, *args, **kwargs):
        if 'beanstalkd_host' in kwargs:
            self.beanstalkd_host = kwargs['beanstalkd_host']
            del(kwargs['beanstalkd_host'])

        if 'beanstalkd_port' in kwargs:
            self.beanstalkd_port = kwargs['beanstalkd_port']
            del(kwargs['beanstalkd_port'])

        Command.__init__(self, *args, **kwargs)


    def _format_uptime(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return u'{0}h {1}m {2}s'.format(hours, minutes, seconds)
