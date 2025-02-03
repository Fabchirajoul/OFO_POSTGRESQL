import psycopg2

def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname="OFO_DATABASE",
            user="postgres",
            password="219050918@Rajour",
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        print("Error connecting to PostgreSQL database:", e)
        return None

# Establish a global database connection
conn = get_db_connection()

def search_for_job_codes(id):
    """Search for job codes using a given ID."""
    try:
        if conn:
            cursor = conn.cursor()

            query = """
                SELECT occupation_id as id, specialization_id, LOWER(specialization_title) AS job_title, 'specialization' AS source 
                FROM specialization WHERE occupation_id = %s

                UNION

                SELECT unit_id as id, occupation_id, LOWER(occupation_title) AS job_title, 'occupation' AS source 
                FROM occupation WHERE unit_id = %s
            """

            cursor.execute(query, (id, id))

            column_names = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()

            return [dict(zip(column_names, row)) for row in rows]
        else:
            print("No valid connection.")
            return None
    except Exception as e:
        print(f"Error executing query: {e}")
        return None


def search_for_job_titles(conn, title):
    """Search job titles using a case-insensitive search."""
    try:
        if conn:
            cursor = conn.cursor()

            query = """
                SELECT occupation_id AS id, occupation_id AS ofo_code, LOWER(specialization_title) AS job_title, 'specialization' AS source
                FROM specialization
                WHERE LOWER(specialization_title) LIKE LOWER(%s)

                UNION

                SELECT unit_id AS id, occupation_id AS ofo_code, LOWER(occupation_title) AS job_title, 'occupation' AS source
                FROM occupation
                WHERE LOWER(occupation_title) LIKE LOWER(%s)
            """

            cursor.execute(query, (f"%{title}%", f"%{title}%"))

            column_names = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()

            result = [dict(zip(column_names, row)) for row in rows]
            return find_word_in_job_titles(title, result) if result else result
        else:
            print("No valid connection.")
            return None
    except Exception as e:
        print(f"Error executing query: {e}")
        return None


def search_for_job_titles_abbreviation(conn, title):
    """Search job titles using abbreviations (Initials)."""
    try:
        if conn:
            cursor = conn.cursor()

            query = """
                SELECT occupation_id AS id, occupation_id AS ofo_code, LOWER(specialization_title) AS job_title, 'specialization' AS source
                FROM specialization
                WHERE (
                    LOWER(LEFT(specialization_title, 1)) || 
                    LOWER(SUBSTRING(specialization_title FROM POSITION(' ' IN specialization_title) + 1 FOR 1))
                ) = %s
                AND LENGTH(specialization_title) > 8

                UNION 

                SELECT unit_id AS id, occupation_id AS ofo_code, LOWER(occupation_title) AS job_title, 'occupation' AS source
                FROM occupation
                WHERE (
                    LOWER(LEFT(occupation_title, 1)) || 
                    LOWER(SUBSTRING(occupation_title FROM POSITION(' ' IN occupation_title) + 1 FOR 1))
                ) = %s
                AND LENGTH(occupation_title) > 8
            """

            cursor.execute(query, (title, title))

            column_names = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()

            result = [dict(zip(column_names, row)) for row in rows]
            return find_word_in_job_titles(title, result) if result else result
        else:
            print("No valid connection.")
            return None
    except Exception as e:
        print(f"Error executing query: {e}")
        return None


def search_for_job_titles_with_ofo_code(conn, ofo_code):
    """Search job titles using OFO codes."""
    try:
        if conn:
            cursor = conn.cursor()

            query = """
                SELECT occupation_id AS ofo_code, LOWER(specialization_title) AS job_title, 'specialization' AS source
                FROM specialization
                WHERE occupation_id = %s

                UNION

                SELECT occupation_id AS ofo_code, LOWER(occupation_title) AS job_title, 'occupation' AS source
                FROM occupation
                WHERE occupation_id = %s
            """

            cursor.execute(query, (ofo_code, ofo_code))

            column_names = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()

            return [dict(zip(column_names, row)) for row in rows] if rows else []
        else:
            print("No valid connection.")
            return None
    except Exception as e:
        print(f"Error executing query: {e}")
        return None


def find_word_in_job_titles(word, data):
    """Find words in job titles."""
    return [item for item in data if word.lower() in item['job_title'].lower()]


def search_for_job_titles_for_model(conn, title):
    """
    Search for a specific job title (case-insensitive) across multiple tables and return matching rows with all columns.
    """
    if isinstance(title, list):
        output = []
        for item in title:
            try:
                if conn:
                    cursor = conn.cursor()
                    query = """
                    SELECT occupation_id AS id, occupation_id AS ofo_code, LOWER(specialization_title) AS job_title, 'specialization' AS source
                    FROM specialization
                    WHERE LOWER(specialization_title) LIKE LOWER(%s)

                    UNION

                    SELECT unit_id AS id, occupation_id AS ofo_code, LOWER(occupation_title) AS job_title, 'occupation' AS source
                    FROM occupation
                    WHERE LOWER(occupation_title) LIKE LOWER(%s)

                    UNION

                    SELECT minor_id AS id, unit_id AS ofo_code, LOWER(unit_title) AS job_title, 'unit' AS source
                    FROM unit
                    WHERE LOWER(unit_title) LIKE LOWER(%s)
                    """

                    cursor.execute(query, (f"%{item}%", f"%{item}%", f"%{item}%"))

                    column_names = [desc[0] for desc in cursor.description]
                    rows = cursor.fetchall()
                    result = [dict(zip(column_names, row)) for row in rows]

                    if result:
                        output.append(result[0])

                else:
                    print("No valid connection.")
                    return None
            except Exception as e:
                print(f"Error executing query: {e}")
                return None

        return output if output else []
    else:
        try:
            if conn:
                cursor = conn.cursor()
                query = """
                SELECT occupation_id AS id, occupation_id AS ofo_code, LOWER(specialization_title) AS job_title, 'specialization' AS source
                FROM specialization
                WHERE LOWER(specialization_title) LIKE LOWER(%s)

                UNION

                SELECT unit_id AS id, occupation_id AS ofo_code, LOWER(occupation_title) AS job_title, 'occupation' AS source
                FROM occupation
                WHERE LOWER(occupation_title) LIKE LOWER(%s)

                UNION

                SELECT minor_id AS id, unit_id AS ofo_code, LOWER(unit_title) AS job_title, 'unit' AS source
                FROM unit
                WHERE LOWER(unit_title) LIKE LOWER(%s)
                """

                cursor.execute(query, (f"%{title}%", f"%{title}%", f"%{title}%"))

                column_names = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                result = [dict(zip(column_names, row)) for row in rows]

                return result if result else []
            else:
                print("No valid connection.")
                return None
        except Exception as e:
            print(f"Error executing query: {e}")
            return None

