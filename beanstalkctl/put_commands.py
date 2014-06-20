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
            self.respond('Please specify a tube')
            return False

        tube = args[-1]

        try:

            self.respond('Put a message onto tube "{0}":'.format(tube))

            if tube not in self.beanstalkd.tubes():
                self.respond(
                    '  tube {0} does not exist and will be created'.format(tube)
                )

            priority = self.request(
                '  priority (default: {0}): '.format(2**31),
                default=None
            )

            delay = self.request(
                '  delay (default: 0): ',
                default=0
            )

            ttr = self.request(
                '  time-to-run (default: 120s): ',
                default=None
            )

            body = self.request(
                '  body (ctrl+d to continue):',
                default="",
                stream=True,
            )

            self.respond("""

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
))

            if not self.user_wants_to_continue():
                return self.cancel()

            self.beanstalkd.use(tube)

            kwargs = {}

            if priority:
                kwargs['priority'] = priority

            if delay:
                kwargs['delay'] = int(delay)

            if ttr:
                kwargs['ttr'] = int(ttr)

            jid = self.beanstalkd.put(body, **kwargs)

            self.respond('Successfully created job: {0}'.format(jid))

        except KeyboardInterrupt:
            _print('Cancelling put operation.')
            return False
