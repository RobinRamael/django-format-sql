import unittest
from datetime import datetime

from django.conf import settings
from django.db import DEFAULT_DB_ALIAS, connection, connections
from django.db.migrations.executor import MigrationExecutor
from django.test import TransactionTestCase
from django.test.utils import CaptureQueriesContext
from django.utils import timezone

import sqlparse
from webtest.forms import Text


class FormattedNumQueriesMixin:

    def assertNumQueries(self, num, func=None, *args, **kwargs):
        """
        Overrides TestCase.assertNumQueries to print error messages in SQL
        format.
        """
        using = kwargs.pop("using", DEFAULT_DB_ALIAS)
        conn = connections[using]

        context = _AssertNumQueriesContext(self, num, conn)
        if func is None:
            return context

        with context:
            func(*args, **kwargs)

    def assertMaxNumQueries(self, up, func=None, *args, **kwargs):
        """
        Assertion to test the max number of queries that will be executed.
        """
        using = kwargs.pop("using", DEFAULT_DB_ALIAS)
        conn = connections[using]

        context = _assertMaxNumQueriesContext(self, up, conn)
        if func is None:
            return context

        with context:
            func(*args, **kwargs)


class _AssertNumQueriesContext(CaptureQueriesContext):
    def __init__(self, test_case, num, connection):
        self.test_case = test_case
        self.num = num
        super(_AssertNumQueriesContext, self).__init__(connection)

    def __exit__(self, exc_type, exc_value, traceback):
        super(_AssertNumQueriesContext, self).__exit__(exc_type, exc_value,
                                                       traceback)

        if exc_type is not None:
            return

        executed = len(self)

        self.test_case.assertEqual(
            executed, self.num,
            "%d queries executed, %d expected\nCaptured queries were:\n%s" % (
                executed, self.num,
                '\n\n\n'.join(
                    "################ Query " + str(num) + " ################"
                    + '\n\n' +
                    sqlparse.format(q['sql'], reindent=True)
                    for num, q in enumerate(self.captured_queries)
                )
            )
        )
