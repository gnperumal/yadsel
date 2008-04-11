from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from optparse import make_option
from imp import find_module, load_module

from yadsel.execution import AVAILABLE_ACTIONS, AVAILABLE_MODES, do
from yadsel import core, drivers

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--action', action='store', dest='action', default='up',
            type='choice', choices=AVAILABLE_ACTIONS,
            help='Action of evolution; up=upgrade, down=downgrade'),
        make_option('--from', action='store', dest='from', default=0,
            help=''),
        make_option('--to', action='store', dest='to', default=0,
            help=''),
        make_option('--mode', action='store', dest='mode', default='steps',
            type='choice', choices=AVAILABLE_MODES,
            help='Mode of output; hidden=messages are hidden, steps=step by step, interactive=confirms actions, output=only prints to output'),
        make_option('--test', action='store', dest='test', default=False,
            type='choice', choices=[True, False],
            help='Set test mode'),
        make_option('--history', action='store', dest='history', default=True,
            type='choice', choices=[True, False],
            help='Write history of versions'),
        make_option('--silent', action='store', dest='silent', default=False,
            type='choice', choices=[True, False],
            help='Keeps exception messages'),
        make_option('--log', action='store', dest='log', default=True,
            type='choice', choices=[True, False],
            help='Write a log of changes'),
    )
    help = 'Executes Yadsel database version control for the given app name(s).'
    args = '[appname ...]'

    def handle(self, *app_labels, **options):
        from django.db import models
        if not app_labels:
            raise CommandError('Enter at least one appname.')

        try:
            # Get applications list
            app_list = [app for app in settings.INSTALLED_APPS if app.split('.')[-1] in app_labels]

            #app_list = [models.get_app(app_label) for app_label in app_labels]
        except (ImproperlyConfigured, ImportError), e:
            raise CommandError("%s. Are you sure your INSTALLED_APPS setting is correct?" % e)

        output = []
        for app in app_list:
            # Get versions module as versions_path
            module = self.find_versions_module(app)

            app_output = self.handle_app(app.split('.')[-1], module, **options)

            if app_output:
                output.append(app_output)

        return '\n'.join(output)

    def handle_app(self, app_label, app, **options):
        from django.conf import settings
        from django.db import connection

        # driver
        driver_type = self.__get_driver()

        # dsn
        dsn = self.__get_dsn(driver_type)
        
        # user
        user = getattr(settings, 'DATABASE_USER', None)

        # pass
        passwd = getattr(settings, 'DATABASE_PASSWORD', None)

        # action
        action = options.get('action', 'up')

        # current_version
        current_version = options.get('from', 0)

        # new_version
        new_version = options.get('to', 0)

        # mode
        mode = options.get('mode', 'steps')

        # test - settings
        test = options.get('test', getattr(settings, 'YADSEL_TEST', False))

        # history - settings
        history = options.get('history', getattr(settings, 'YADSEL_HISTORY', True))

        # silent - settings
        silent = options.get('silent', getattr(settings, 'YADSEL_SILENT', False))

        # log - settings
        log = options.get('log', getattr(settings, 'YADSEL_LOG', True))

        # Run
        do(versions_path=app,
               driver_type=driver_type,
               dsn=dsn,
               action=action,
               user=user,
               passwd=passwd,
               current_version=current_version,
               new_version=new_version,
               mode=mode,
               test=test,
               history=history,
               silent=silent,
               log=log,
               version_space=app_label,
               )

    def find_versions_module(self, app_name):
        parts = app_name.split('.')
        parts.append('yadsel_versions')
        parts.reverse()
        path = None

        try:
            while parts:
                part = parts.pop()
                f, path, descr = find_module(part, path and [path] or None)

            module = load_module('yadsel_versions', f, path, descr)
            return module
        except ImportError, e:
            return None

    def __get_driver(self):
        return drivers.DRIVERS_PER_ENGINE[getattr(settings, 'DATABASE_ENGINE', '')]

    def __get_dsn(self, driver_type=None):
        if driver_type == 'sqlite':
            dsn = settings.DATABASE_NAME
        else:
            dsn = ''
            if getattr(settings, 'DATABASE_ENGINE', ''): dsn += settings.DATABASE_HOST
            if getattr(settings, 'DATABASE_PORT', ''): dsn += ':'+settings.DATABASE_PORT
            if getattr(settings, 'DATABASE_NAME', ''): dsn += '/'+settings.DATABASE_NAME

        return dsn

