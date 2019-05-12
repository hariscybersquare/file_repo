import psycopg2
from django.db import connection
# from django import db


class DbModel():
    """
    Created to update to the database.
    """

    def update_database(self, filedetails):
        try:
            # Print PostgreSQL Connection properties
            # The size of the file can be big later.
            cur = connection.cursor()
            cur.execute("select * from\
                         information_schema.tables\
                         where table_name=%s", ('file_repo',))
            cur.close()
            if not bool(cur.rowcount):
                create_table_query = '''CREATE TABLE file_repo
                                      (
                                      name  TEXT  PRIMARY KEY   NOT NULL,
                                      filepath TEXT    NOT NULL,
                                      creationdatetime    timestamp NOT NULL,
                                      modificationdatetime timestamp NOT NULL,
                                      size           bigint    NOT NULL ,
                                      archived BOOLEAN)'''
                cursor = connection.cursor()
                cursor.execute(create_table_query)
                connection.commit()
                cursor.close()
            curupdate = connection.cursor()
            args_str = ','.join(
                               curupdate.mogrify("(%s,%s,%s,%s,%s,%s)", x)
                               .decode("utf-8") for x in filedetails)
            update_table_query = "INSERT INTO file_repo (name,\
                                                        filepath,\
                                                        creationdatetime,\
                                                        modificationdatetime,\
                                                        size, archived)\
                                  VALUES " + args_str + "\
                                  ON CONFLICT (name)\
                                  DO UPDATE SET\
                                  ( filepath,\
                                  creationdatetime,\
                                  modificationdatetime, \
                                  size,\
                                  archived) = \
                                              (EXCLUDED.filepath, \
                                               EXCLUDED.creationdatetime, \
                                               EXCLUDED.modificationdatetime,\
                                               EXCLUDED.size,\
                                               EXCLUDED.archived)"
            curupdate.execute(update_table_query)
            connection.commit()
            curupdate.close()
            # The following code can be used to find out the time
            # of database query execution.
            # for query in db.connections['default'].queries:
            #   print(query['time'])
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
