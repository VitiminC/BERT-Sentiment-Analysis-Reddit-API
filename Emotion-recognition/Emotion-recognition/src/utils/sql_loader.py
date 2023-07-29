from src.config.config import *

class DataSqlLoader:
    def __init__(self):
        # connect to personal mysql server
        self.db = pymysql.Connect(
            host=MYSQL_HOST,
            user=MYSQL_USERNAME,
            passwd=MYSQL_PASSWORD,
            db=MYSQL_DATABASE,
            port=MYSQL_PORT)
        self.c = self.db.cursor()

    def creat_table(self):
        try:
            self.c.execute('''
                        create table comment_table
                            (
                                ID                     int auto_increment
                                    primary key,
                                Title                  text     not null,
                                Images                 text     not null,
                                SubmissionCreatTime    datetime not null,
                                SubmissionRetrieveTime datetime not null,
                                Commenter              text     not null,
                                Comment                text     not null,
                                CommentCreatTime       datetime not null,
                                CommentRetrieveTime    datetime not null,
                                Status                 text     not null,
                                Score                  int      not null,
                                ControversialityScale  int      not null
                            );
                        ''')
        except Exception as e:
            print(e)

    def insert_into_tables(self, filename, tablename):
        query = '''
            LOAD DATA INFILE '{}'
                INTO TABLE {} fields terminated by ',' lines terminated by '\r\n'
            '''.format(filename, tablename)
        try:
            print(query)
            # self.c.execute(query)
        except Exception as e:
            print(e)

    def drop_table(self, tablename):
        try:
            self.c.execute("drop table {}".format(tablename))
        except Exception as e:
            print(e)

    def get_sample(self, table, limit=None):
        if limit == None:
            query = 'SELECT * FROM {};'.format(table)
        else:
            query = 'SELECT * FROM {} limit {};'.format(table, limit)
            pd.read_sql(sql=query, con=self.db)
        return pd.read_sql(sql=query, con=self.db)

    def sql_query(self, query):
        try:
            return pd.read_sql(sql=query, con=self.db)
        except Exception as e:
            print(e)

    def close(self):
        self.db.close()


