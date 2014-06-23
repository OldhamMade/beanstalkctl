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



class BaseSpec(unittest.TestCase):
    BEANSTALKD_INSTANCE = None
    BEANSTALKD_HOST = '127.0.0.1'
    BEANSTALKD_PORT = 11411

    def _beanstalkd_path(self):
        beanstalkd = os.getenv('BEANSTALKD')

        if beanstalkd:
            return os.path.abspath(os.path.join(
                os.path.dirname(__file__),
                '..', beanstalkd))

        # assume beanstalkd is
        # installed globally
        return 'beanstalkd'

    BEANSTALKD_PATH = property(_beanstalkd_path)

    def _start_beanstalkd(self):
        print "Using beanstalkd: {0}".format(self.BEANSTALKD_PATH)
        print "Starting up the beanstalkd instance...",
        self.BEANSTALKD_INSTANCE = subprocess.Popen(
            [self.BEANSTALKD_PATH, '-p', str(self.BEANSTALKD_PORT)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
        )
        print 'running as {0}...'.format(self.BEANSTALKD_INSTANCE),
        print "done."

    def base_setup(self):
        self._start_beanstalkd()

        beanstalkctl = ' '.join([
            os.path.join(
                os.path.dirname(self.call('pwd')),
                'bin',
                'beanstalkctl'),
            '--host={0}'.format(self.BEANSTALKD_HOST),
            '--port={0}'.format(self.BEANSTALKD_PORT), ])

        self.logfh = open(
            '{0}.log'.format(self.__class__.__name__), 'w', 0)

        self.beanstalkctl = pexpect.spawn(beanstalkctl, logfile=self.logfh)

        self.beanstalkctl.setecho(False)
        self.beanstalkctl.expect('beanstalkctl> ')


    def base_teardown(self):
        self.logfh.close()

        if not self.BEANSTALKD_INSTANCE:
            return

        print "Shutting down the beanstalkd instance...",
        self.BEANSTALKD_INSTANCE.terminate()
        print "done."


    def interact(self, cmd):
        self.beanstalkctl.sendline(cmd)
        self.beanstalkctl.expect_exact('beanstalkctl> ')
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



class BasicSpec(BaseSpec):
    def setUp(self):
        self.base_setup()
        self.conn = beanstalkc.Connection(
            host=self.BEANSTALKD_HOST,
            port=self.BEANSTALKD_PORT)

    def tearDown(self):
        self.base_teardown()

    def ensure_beanstalkd_exists(self):
        self.assertTrue(self.BEANSTALKD_PATH)

    def ensure_beanstalkd_starts(self):
        self.assertTrue(self.conn)

    def ensure_beanstalkctl_responds(self):
        result = self.interact('help')
        self.assertTrue(result.strip())
