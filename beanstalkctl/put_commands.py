import sys
from ishell.utils import _print
from .base import BaseCommand


class PutCommand(BaseCommand):
    __cmd__ = 'put'
    __help__ = 'put a message onto a queue'

    def args(self):
        return self.beanstalkd.tubes()

    def run(self, line):
        args = line.split()

        if not len(args) == 2:
            print 'Please specify a tube'
            return

        tube = args[-1]

        try:

            print 'Put a message onto tube "{0}":'.format(tube)

            if tube not in self.beanstalkd.tubes():
                print '  tube {0} does not exist and will be created'.format(tube)

            priority = raw_input('  priority (default: {0}): '.format(2**31)) \
                       or None

            delay = raw_input('  delay (default: 0): ') \
                    or 0

            ttr =  raw_input('  time-to-run (default: 120s): ') \
                   or None

            print '  body (ctrl+d to continue):'
            body = '\n'.join([l.strip() for l in sys.stdin.readlines()])

            print """

Confirm job:
  tube: {tube}
  priority: {priority}
  delay: {delay}s
  ttr: {ttr}s
--body:--
{body}
---------
""".format(
    tube=tube,
    priority=priority,
    delay=delay,
    ttr=ttr if ttr else 120,
    body=body,
)

            response = raw_input('Do you wish to continue? y/N\n')

            if response.lower() not in ('y', 'yes'):
                print 'Cancelled.'
                return
            self.beanstalkd.use(tube)

            kwargs = {}

            if priority:
                kwargs['priority'] = priority

            if delay:
                kwargs['delay'] = int(delay)

            if ttr:
                kwargs['ttr'] = int(ttr)

            jid = self.beanstalkd.put(body, **kwargs)

            print 'Successfully created job: {0}'.format(jid)
        except KeyboardInterrupt:
            _print('Cancelling put operation.')
            return
