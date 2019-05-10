import psycopg2
from django.db import connection

class DbModel():
  """
  Created to update to the database.
  """
  def update_database(self, filedetails):
      try:
          # Print PostgreSQL Connection properties
          #The size of the file can be big later.
          cur = connection.cursor()
          cur.execute("select * from information_schema.tables where table_name=%s",('file_repo',))
          cur.close()
          if bool(cur.rowcount):
              pass
          else:
              create_table_query = '''CREATE TABLE file_repo
                                    (
                                    name           TEXT  PRIMARY KEY   NOT NULL,
                                    filepath           TEXT    NOT NULL,
                                    creationdatetime           timestamp    NOT NULL,
                                    modificationdatetime           timestamp    NOT NULL,
                                    size           bigint    NOT NULL ,
                                    archived BOOLEAN)'''
              cursor = connection.cursor()
              cursor.execute(create_table_query)
              connection.commit()
              cursor.close()
          curupdate = connection.cursor()
          update_table_query = '''INSERT INTO file_repo 
                                        (name, 
                                         filepath,
                                         creationdatetime,
                                         modificationdatetime,
                                         size,
                                         archived)
                                  VALUES
                                  (%s, %s, %s, %s,%s, %s)
                                   ON CONFLICT (name) 
                                     DO
                                       UPDATE
                                       SET ( 
                                        filepath,
                                        creationdatetime,
                                        modificationdatetime,
                                        size,
                                        archived) = (EXCLUDED.filepath, 
                                                    EXCLUDED.creationdatetime, 
                                                    EXCLUDED.modificationdatetime,
                                                    EXCLUDED.size,
                                                    EXCLUDED.archived)
                                      '''
          curupdate.execute(update_table_query, (filedetails['name'],filedetails['filepath'],
                                                 filedetails['creationdatetime'], filedetails['modificationdatetime'],
                                                 filedetails['size'], filedetails['archived']))
          connection.commit()
          curupdate.close()
          print("updated the database... ")
      except (Exception, psycopg2.Error) as error :
          print ("Error while connecting to PostgreSQL", error)

