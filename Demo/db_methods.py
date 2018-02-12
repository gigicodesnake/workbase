'''
Created on 08 Feb 2018

@author: Gigi
'''
from configparser import ConfigParser
from pypika import Query, Table, Field
import psycopg2
import pandas as pd
 
 
def config(filename='database.ini', section='postgresql') -> dict:
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
 
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
 
    return db

def portal():
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        
        return conn
        
    except (Exception, psycopg2.DatabaseError) as error:
        print('error in db_methods.py-connect_to_database()-function')
        print(error)
        conn.close()

def input_into_orders_table(input_list):
    
    with portal() as conn:
        with conn.cursor() as cur:
            try:
                customers = Table('lab_orders_table')
                q = Query.into(customers).columns('item_name', 'catalogue_number', 'cas_number', 'manufacturer', 'supplier', 'price', 'unit_quantity', 'amount_ordered', 'end_user', 'order_reference', 'order_status', 'notes').insert(
                    input_list[0],input_list[1] , input_list[2], input_list[3], input_list[4], input_list[5], input_list[6], input_list[7], input_list[8], input_list[9], input_list[10], input_list[11])

                cur.execute(str(q))
     
            except (Exception, psycopg2.DatabaseError) as error:
                print('error in db_methods.py-connect_to_database()-function')
                print(error)
                cur.close()      

def reset_orders_id():
    with portal() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("TRUNCATE TABLE lab_orders_table RESTART IDENTITY")
     
            except (Exception, psycopg2.DatabaseError) as error:
                print('error in db_methods.py-connect_to_database()-function')
                print(error)
                cur.close()   
    
def view_table (table_name, field_list):
       
    if not field_list:
        with portal() as conn:
            with conn.cursor() as cur:
                try:
                    table = Table(table_name)
                    q = Query.from_(table).select('*')
                    q = str(q)
                    df = pd.read_sql_query(q, conn)
                    print(df)
                except (Exception, psycopg2.DatabaseError) as error:
                    print('error in db_methods.py-connect_to_database()-function')
                    print(error)
                    cur.close()
    else:
        with portal() as conn:
            with conn.cursor() as cur:
                try:
                    table = Table(table_name)
                    q = Query.from_(table).select(field_list)
                    q = str(q)
                    df = pd.read_sql_query(q, conn)
                except (Exception, psycopg2.DatabaseError) as error:
                    print('error in db_methods.py-connect_to_database()-function')
                    print(error)
                    cur.close()
        



