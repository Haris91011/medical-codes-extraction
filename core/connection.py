from core.config import settings
import pyodbc
import streamlit as st

MSSQL_SERVER =settings.MSSQL_SERVER
MSSQL_DATABASE= settings.MSSQL_DATABASE
MSSQL_USER= settings.MSSQL_USER
MSSQL_PASSWORD= settings.MSSQL_PASSWORD




    

def get_db_connection():
    try:
        drivers = ['{SQL Server}', '{ODBC Driver 17 for SQL Server}']
        for driver in drivers:
            try:
                conn_str = (
                    f'DRIVER={driver};'
                    f'SERVER={MSSQL_SERVER};'
                    f'DATABASE={MSSQL_DATABASE};'
                    f'UID={MSSQL_USER};'
                    f'PWD={MSSQL_PASSWORD}'
                )
                return pyodbc.connect(conn_str)
            except pyodbc.Error:
                continue
        raise Exception("No working driver found")
    except Exception as e:
        return None
    


@st.cache_data(ttl=3600)
def load_all_icd_codes():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                SELECT code 
                FROM MedicalCodes 
                WHERE code_type = 'icd'
            """
            cursor.execute(query)
            results = cursor.fetchall()
            return [(str(row[0]), str(row[0])) for row in results]
        except Exception as e:
            st.error(f"Error fetching ICD codes: {e}")
            return []
        finally:
            connection.close()
    return []


@st.cache_data(ttl=3600)
def load_all_cpt_codes():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                SELECT code 
                FROM MedicalCodes 
                WHERE code_type = 'cpt'
            """
            cursor.execute(query)
            results = cursor.fetchall()
            return [(str(row[0]), str(row[0])) for row in results]
        except Exception as e:
            st.error(f"Error fetching CPT codes: {e}")
            return []
        finally:
            connection.close()
    return []