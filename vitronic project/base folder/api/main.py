from fastapi import FastAPI, HTTPException
from api import database
app = FastAPI()


@app.get("/data/")
def read_data():
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_registration LIMIT 100")
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    return {"columns": column_names, "data": rows}
