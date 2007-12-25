from django.core.management.base import BaseCommand
from optparse import make_option

from yadsel.execution import AVAILABLE_ACTIONS, AVAILABLE_MODES, do

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--action', action='store', dest='verbosity', default='up',
            type='choice', choices=AVAILABLE_ACTIONS,
            help='Action of evolution; up=upgrade, down=downgrade'),
        make_option('--from', action='store', dest='interactive', default=0,
            help=''),
        make_option('--to', action='store', dest='interactive', default=0,
            help=''),
        make_option('--mode', action='store', dest='verbosity', default='steps',
            type='choice', choices=AVAILABLE_MODES,
            help='Mode of output; hidden=messages are hidden, steps=step by step, interactive=confirms actions, output=only prints to output'),
        make_option('--test', action='store', dest='verbosity', default=False,
            type='choice', choices=[True, False],
            help='Set test mode'),
        make_option('--history', action='store', dest='verbosity', default=True,
            type='choice', choices=[True, False],
            help='Write history of versions'),
        make_option('--silent', action='store', dest='verbosity', default=False,
            type='choice', choices=[True, False],
            help='Keeps exception messages'),
        make_option('--log', action='store', dest='verbosity', default=True,
            type='choice', choices=[True, False],
            help='Write a log of changes'),
    )
    help = 'Executes Yadsel database version control for the given app name(s).'
    args = '[appname ...]'

    def handle(self, *test_labels, **options):
        from django.conf import settings
        from django.db import connection

        # Gets driver, dsn, user and pass
        driver = self.__get_driver()
        dsn = self.__get_dsn()

        # action
        action = options.get('action', 'up')

        # current_version
        current_version = options.get('from', 0)

        # new_version
        new_version = options.get('to', 0)

        # mode
        mode = options.get('mode', 'steps')

        # test - settings
        test = options.get('test', settings.__dict__.get('YADSEL_TEST', False))

        # history - settings
        history = options.get('history', settings.__dict__.get('YADSEL_HISTORY', True))

        # silent - settings
        silent = options.get('silent', settings.__dict__.get('YADSEL_SILENT', False))

        # log - settings
        log = options.get('log', settings.__dict__.get('YADSEL_LOG', True))

        # Loop for applications
        # - versions_path
        # - Run

        print test_labels
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

    def __get_driver(self):
        pass

    def __get_dsn(self):
        pass

