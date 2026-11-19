"""
Django Management Command: python manage.py save_to_mongodb
Exports all donor records and system metadata to MongoDB Atlas.
"""

from django.core.management.base import BaseCommand
import sys
from pathlib import Path

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

from save_to_mongodb import build_mongo_uri, sync_to_mongodb, DEFAULT_DB_NAME, DEFAULT_BASE_URI


class Command(BaseCommand):
    help = 'Exports all registered donor data from SQLite to MongoDB Atlas.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--password',
            '-p',
            type=str,
            help='MongoDB Atlas user password for krishnaadithyan599_db_user'
        )
        parser.add_argument(
            '--uri',
            '-u',
            type=str,
            default=DEFAULT_BASE_URI,
            help='Full MongoDB Atlas connection URI'
        )
        parser.add_argument(
            '--db',
            '-d',
            type=str,
            default=DEFAULT_DB_NAME,
            help='Target MongoDB database name (default: jeevadhaara)'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Initializing Jeevadhaara MongoDB Atlas Sync..."))
        password = options.get('password')
        raw_uri = options.get('uri')
        db_name = options.get('db')

        try:
            uri = build_mongo_uri(raw_uri, password)
            sqlite_path = str(BASE_DIR / 'db.sqlite3')
            success = sync_to_mongodb(uri, db_name, sqlite_path)
            if success:
                self.stdout.write(self.style.SUCCESS("Data successfully synced to MongoDB Atlas!"))
            else:
                self.stdout.write(self.style.ERROR("MongoDB Atlas sync failed. Please check credentials."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error during export: {e}"))
