from django.core.management.base import BaseCommand
from django.db import connection
from pathlib import Path
import os

class Command(BaseCommand):
     help = 'It will populate the collection table'

     def handle(self, *args, **options) -> str | None:
          print("Populating Collection Table....")
          current_dir =os.path.dirname( __file__)
          file_path = os.path.join(current_dir, 'queryInsert.sql')
          sql = Path(file_path).read_text()
          with connection.cursor() as cursor:
              cursor.execute(sql=sql)