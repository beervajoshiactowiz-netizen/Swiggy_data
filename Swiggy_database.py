import json
import mysql.connector


def send_to_db(extracted):
    try:
        # Connect to MySQL Server (without specifying a database yet)
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="actowiz"
        )
        cursor = conn.cursor()

        # 1. Create the database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS swiggy_db")

        # 2. IMPORTANT: Switch to the database you just created
        cursor.execute("USE swiggy_db")

        # 3. Create the table inside 'swiggy_db'
        create_query = """
                CREATE TABLE IF NOT EXISTS Swiggy_items(
                Name VARCHAR(255),
                ProductId VARCHAR(50),
                Price FLOAT,
                Quantity VARCHAR(50),
                ImageUrl JSON,
                Discount INT,
                Mrp FLOAT,
                InStock BOOLEAN
                );
        """
        cursor.execute(create_query)

        # 4. Insert Query
        insert_query = """
        INSERT INTO Swiggy_items(
            Name, ProductId, Price, Quantity, ImageUrl, Discount, Mrp, InStock
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        # 5. Efficient Bulk Insert
        data_to_insert = []
        for f in extracted:
            data_to_insert.append((
                f.get("name"),
                f.get("Prod_id"),
                f.get("Prod_price"),
                f.get("Prod_quantity"),
                json.dumps(f.get("Image_URL")),  # Ensure valid JSON format
                f.get("Discount_per"),
                f.get("mrp"),
                f.get("In_stock")
            ))

        if data_to_insert:
            cursor.executemany(insert_query, data_to_insert)
            conn.commit()  # Save changes to the database
            print(f"Successfully inserted {cursor.rowcount} records.")
        else:
            print("No data found to insert.")

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")

    finally:
        # Always close the cursor and connection
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
