import psycopg2
from django.db import connection
from datetime import datetime


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
            if not bool(cur.rowcount):
                create_table_query = '''CREATE TABLE file_repo
                                (
                                file_name  TEXT  PRIMARY KEY   NOT NULL,
                                file_path TEXT    NOT NULL,
                                file_creation_date_time timestamp NOT NULL,
                                file_modification_date_time timestamp NOT NULL,
                                size           bigint    NOT NULL ,
                                archived BOOLEAN NOT NULL,
                                created_datetime timestamp NOT NULL,
                                updated_datetime timestamp NOT NULL)'''
                cursor = connection.cursor()
                cursor.execute(create_table_query)
                connection.commit()
                cursor.close()
            cur.close()
            curupdate = connection.cursor()
            args_str = ','.join(
                             curupdate.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s)", x)
                             .decode("utf-8") for x in filedetails)
            update_table_query = "INSERT INTO file_repo (file_name,\
                                                        file_path,\
                                                        file_creation_date_time,\
                                                        file_modification_date_time,\
                                                        size, archived,\
                                                        created_datetime,\
                                                        updated_datetime)\
                                  VALUES " + args_str + "\
                                  ON CONFLICT (file_name)\
                                  DO UPDATE SET\
                                  ( file_path,\
                                  file_modification_date_time, \
                                  size,\
                                  archived, updated_datetime) = \
                                              (EXCLUDED.file_path, \
                                               EXCLUDED.file_modification_date_time,\
                                               EXCLUDED.size,\
                                               EXCLUDED.archived,\
                                               EXCLUDED.updated_datetime)"
            curupdate.execute(update_table_query)
            connection.commit()
            curupdate.close()
            # The following code can be used to find out the time
            # of database query execution.
            # for query in db.connections['default'].queries:
            #   print(query['time'])
        except (Exception, psycopg2.Error) as error:
            print("Error while querying in the PostgreSQL", error)
        finally:
            if curupdate:
                curupdate.close()
            if cur:
                cur.close()

    def get_last_updated_datetime(self):
        '''
        This function will return the last updated datetime in the database.
        '''
        try:
            cur = connection.cursor()
            cur.execute("SELECT updated_datetime FROM file_repo\
                         ORDER BY updated_datetime DESC LIMIT 1")
            if bool(cur.rowcount):
                updated_datetime = cur.fetchall()
                return updated_datetime[0][0]
            else:
                '''
                Just added the following code to make sure that the return
                object is of type datetime.
                '''
                return datetime(1000, 3, 10, 0, 0)

            cur.close()
        except (Exception, psycopg2.Error) as error:
            print("Some error while querying the database.", error)
        finally:
            if cur:
                cur.close()
