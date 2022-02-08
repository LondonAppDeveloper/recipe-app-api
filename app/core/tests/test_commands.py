from unittest.mock import patch, MagicMock

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""
        conn = MagicMock(return_value=None)
        with patch('django.db.utils.ConnectionHandler.__getitem__', return_value=conn):
            call_command('wait_for_db')
            conn.cursor.assert_called_once()

    @patch('time.sleep', return_value=None)
    def test_wait_for_db(self, ts):
        """Test waiting for db"""
        conn = MagicMock(return_value=None)
        with patch('django.db.utils.ConnectionHandler.__getitem__', return_value=conn):
            conn.cursor.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(conn.cursor.call_count, 6)
