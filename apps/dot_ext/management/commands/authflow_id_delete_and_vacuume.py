import time
from django.db import connection

from datetime import date, timedelta
from django.core.management.base import BaseCommand

from apps.dot_ext.models import AuthFlowUuidCopy

DELETE_WITH_LIMIT = "DELETE FROM {table_name} WHERE auth_uuid IN (SELECT auth_uuid FROM {table_name} WHERE created < '{age_date}'::date ORDER BY created LIMIT {limit_on_delete})"
VACUUM_TABLE = "VACUUM FULL {table_name}"


def delete_and_vacuume_auth_uuid_table(age, limit_on_delete, run_vacuum):
    '''
    Delete aged authflow uuid records, and then
    call VACUUM FULL (Postgres only) on table: dot_ext_authflowuuid
    '''

    days_before = date.today()-timedelta(days=age)
    
    delete_sql = DELETE_WITH_LIMIT.format(table_name="dot_ext_authflowuuidcopy", age_date=days_before.strftime("%m/%d/%Y"), limit_on_delete=limit_on_delete)
    vacuum_sql = VACUUM_TABLE.format(table_name="dot_ext_authflowuuidcopy")

    print("delete_sql : {}".format(delete_sql))
    print("vacuum_sql : {}".format(vacuum_sql))

    start_t = time.time()

    aged_records_total = AuthFlowUuidCopy.objects.filter(created__lt=days_before).count()

    print("aged records total = {}".format(aged_records_total))

    with connection.cursor() as cursor:
        cursor.execute(delete_sql)
        end_t = time.time()
        print("query + delete aged records: time elapsed (sec) = {}".format(end_t - start_t))
        if run_vacuum:
            cursor.execute(vacuum_sql)
            end_t = time.time()
            print("query + delete aged records and vacuum table: time elapsed (sec) = {}".format(end_t - start_t))


class Command(BaseCommand):
    help = ('Delete aged dot_ext_authflowuuid table records '
            'and optionally vacuum the table - removing records marked deleted (dead rows) and reclaim space.')
    
    def add_arguments(self, parser):
        parser.add_argument("-a", "--age", type=int, default=30, help="Age (in days) of authflow uuid records qualified for deletion.")
        parser.add_argument("-l", "--limit", type=int, default=30000, help="Limit on number of delete allowed for one run.")
        parser.add_argument("-u", "--vacuum", action="store_true", help="Run Postgress VACUUM FULL after delete")

    def handle(self, *args, **options):
        age = options["age"] if options["age"] else 30
        limit_on_delete = options["limit"] if options["limit"] else 30000
        run_vacuum = options["vacuum"]
        delete_and_vacuume_auth_uuid_table(age, limit_on_delete, run_vacuum)
