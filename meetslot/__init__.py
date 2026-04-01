import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
MySQLdb.version_info = (2, 2, 1, 'final', 0)

try:
    from django.db.backends.mysql.base import DatabaseFeatures
    DatabaseFeatures.minimum_mariadb_version = (10, 0)
    DatabaseFeatures.minimum_database_version = (5, 0)
    DatabaseFeatures.can_return_columns_from_insert = False
    DatabaseFeatures.can_return_rows_from_bulk_insert = False
except Exception:
    pass
