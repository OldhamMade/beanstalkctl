import beanstalkc
from ishell.command import Command


try:
    import re2 as re
except ImportError:
    import re


class BeanstalkdMixin(object):
    """Mixin providing utility functions for
    connecting and publishing to beanstalkd"""

    beanstalkd_host = '0.0.0.0'
    beanstalkd_port = 11300

    def __get_beanstalkd_connection__(self):
        """Obtain a connection to a beanstalkd server"""
        try:
            if not hasattr(self, '_beanstalkd_connection') or \
               not self._beanstalkd_connection:
                self._beanstalkd_connection = beanstalkc.Connection(
                    host=self.beanstalkd_host,
                    port=int(self.beanstalkd_port))
            return self._beanstalkd_connection

        except beanstalkc.SocketError:
            raise Exception(
                'Unable to connect to beanstalkd on {0}:{1}'.format(
                    self.beanstalkd_host,
                    self.beanstalkd_port))

    # beanstalkd property which will reuse or create a beanstalkd connection
    beanstalkd = property(__get_beanstalkd_connection__)



def apply_command_chains(console, chain, **kwargs):
    """Recursively build chained commands from a dictionary"""

    for k, v in chain.iteritems():
        if k[0] == '_':
            continue

        if isinstance(v, dict):
            try:
                help_ = v['__help__']
            except KeyError:
                help_ = 'type `{0}` for further options'.format(k)
            parent = console.addChild(Command(k, help_))
            apply_command_chains(parent, v, **kwargs)
            continue

        cmd = v
        has_args_func = 'args' in cmd.__dict__
        instance = cmd(
            cmd.__cmd__,
            cmd.__help__,
            dynamic_args=has_args_func,
            **kwargs
        )

        console.addChild(instance)

    return console



def natural_sort_key(s, _nsre=re.compile('([0-9]+)')):
    return [int(text) if text.isdigit() else text.lower()
            for text
            in re.split(_nsre, s)]
