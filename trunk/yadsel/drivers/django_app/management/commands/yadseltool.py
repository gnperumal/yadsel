from django.core.management.base import BaseCommand
from django.conf import settings
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

    def handle(self, *test_labels, **options):
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

        # Get applications list
        apps = [a for a in settings.INSTALLED_APPS if not test_labels or a.split('.')[-1] in test_labels]

        # Loop for applications
        for app in apps:
            # Get versions module as versions_path
            module = self.find_versions_module(app)

            if not module: continue
            
            # Run
            do(versions_path=module,
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
               )

        """
        from django.db.models import get_models
        output = []
        app_models = get_models(app)
        app_label = app_models[0]._meta.app_label
        output.append('{%% if perms.%s %%}' % app_label)
        output.append('<div class="module"><h2>%s</h2><table>' % app_label.title())
        for model in app_models:
            if model._meta.admin:
                output.append(MODULE_TEMPLATE % {
                    'app': app_label,
                    'mod': model._meta.module_name,
                    'name': force_unicode(capfirst(model._meta.verbose_name_plural)),
                    'addperm': model._meta.get_add_permission(),
                    'changeperm': model._meta.get_change_permission(),
                })
        output.append('</table></div>')
        output.append('{% endif %}')
        return '\n'.join(output)"""

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
