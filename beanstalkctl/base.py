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


    def user_wants_to_continue(self):
        """Prompt the user for confirmation of command"""
        response = raw_input('Do you wish to continue? y/N\n')
        return response.lower() in ('y', 'yes')


    def print_table(self, rows):
        headers = rows[0]._fields
        lens = []
        for i in range(len(rows[0])):
            lens.append(len(max([x[i] for x in rows] + [headers[i]],
                                key=lambda x: len(str(x)))))
        formats = []
        hformats = []
        for i in range(len(rows[0])):
            if isinstance(rows[0][i], int):
                formats.append("%%%dd" % lens[i])
            else:
                formats.append("%%-%ds" % lens[i])
            hformats.append("%%-%ds" % lens[i])
        pattern = " | ".join(formats)
        hpattern = " | ".join(hformats)
        separator = "-+-".join(['-' * n for n in lens])
        print hpattern % tuple(headers)
        print separator
        for line in rows:
            print pattern % tuple(line)
