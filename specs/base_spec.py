import os
import signal
import subprocess
import beanstalkc
import time
import pexpect

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from beanstalkctl.util import BeanstalkdMixin



class BaseSpec(unittest.TestCase, BeanstalkdMixin):
    beanstalkd_instance = None
    beanstalkd_host = '127.0.0.1'
    beanstalkd_port = 11411

    def _beanstalkd_path(self):
        beanstalkd = os.getenv('BEANSTALKD')

        if beanstalkd:
            return os.path.abspath(os.path.join(
                os.path.dirname(__file__),
                '..', beanstalkd))

        # assume beanstalkd is
        # installed globally
        return 'beanstalkd'

    beanstalkd_path = property(_beanstalkd_path)

    def _start_beanstalkd(self):
        print "Using beanstalkd: {0}".format(self.beanstalkd_path)
        print "Starting up the beanstalkd instance...",
        self.beanstalkd_instance = subprocess.Popen(
            [self.beanstalkd_path, '-p', str(self.beanstalkd_port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
        )
        print 'running as {0}...'.format(self.beanstalkd_instance),
        print "done."

    def base_setup(self):
        self._start_beanstalkd()

        beanstalkctl = ' '.join([
            os.path.join(
                os.path.dirname(self.call('pwd')),
                'bin',
                'beanstalkctl'),
            '--host={0}'.format(self.beanstalkd_host),
            '--port={0}'.format(self.beanstalkd_port), ])

        self.logfh = open(
            '{0}.log'.format(self.__class__.__name__), 'w', 0)

        self.beanstalkctl = pexpect.spawn(beanstalkctl, logfile=self.logfh)

        self.beanstalkctl.setecho(False)
        self.beanstalkctl.expect('beanstalkctl> ')


    def base_teardown(self):
        self.logfh.close()

        if not self.beanstalkd_instance:
            return

        print "Shutting down the beanstalkd instance...",
        self.beanstalkd_instance.terminate()
        print "done."


    def interact(self, cmd, expect='beanstalkctl> '):
        self.beanstalkctl.sendline(cmd)
        self.beanstalkctl.expect_exact(expect)
        return self.get_response()


    def get_response(self):
        result = self.beanstalkctl.before
        if result.endswith('\x1b[K'):
            return result[:-6]
        return result


    def call(self, command, **env):
        """Run a command on the terminal.

        Args:
            command (str): the command to execute

        Keyword Args:
            **env (dict): any keyword arguments are collected into a
            dictionary and passed as environment variables directly
            to the subprocess call.

        Returns:
            tuple.  A tuple containing `(stdoutdata, stderrdata)`, or None
            if unsuccessful.
        """
        p = subprocess.Popen(
            command,
            shell=False,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        result, error = p.communicate()

        if error:
            raise Exception(error)

        return result


    def clean(self, text):
        for chunk in ('\r', r'\\x1b[K'):
            text = text.replace(chunk, '')
        return text.strip()


def skipped(func):
    from nose.plugins.skip import SkipTest
    def wrapper(*args, **kwargs):
        raise SkipTest("Test %s is skipped" % func.__name__)
    wrapper.__name__ = func.__name__
    return wrapper
