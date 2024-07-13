from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List
import psycopg2

conn = psycopg2.connect(
    dbname="mydatabase",
    user="myuser",
    password="mypassword",
    host="localhost",
    port="5432"
)
conn.autocommit = True 

app = FastAPI(
    title="Valuations API",
    description="API to query valuations from Postgre databse",
    version="1.0.0"
)

class Valuations(BaseModel):
    rate_number: str
    legal_description: str
    address: str
    first_owner: str
    use_code: str
    rating_category: str
    market_value: str
    registered_extent: str
    suburb: str
    valuation_roll: str

@app.get("/search_valuations/", response_model=List[Valuations], tags=["valuations"])
def get_search_valuations(
    rate_number: str = Query(None, description="Rate number filter"),
    legal_description: str = Query(None, description="Legal description filter"),
    address: str = Query(None, description="Address filter"),
    first_owner: str = Query(None, description="First owner filter"),
    use_code: str = Query(None, description="Use code filter"),
    rating_category: str = Query(None, description="Rating category filter"),
    market_value: str = Query(None, description="Market value filter"),
    registered_extent: str = Query(None, description="Registered extent filter"),
    suburb: str = Query(None, description="Suburb filter"),
    valuation_roll: str = Query(None, description="Valuation roll filter"),
):
    try:
        filters = []
        params = []

        select_query = """
            SELECT * FROM valuations
            WHERE TRUE
        """

        if rate_number:
            filters.append("rate_number = %s")
            params.append(rate_number)
        if legal_description:
            filters.append("legal_description = %s")
            params.append(legal_description)
        if address:
            filters.append("address = %s")
            params.append(address)
        if first_owner:
            filters.append("first_owner = %s")
            params.append(first_owner)
        if use_code:
            filters.append("use_code = %s")
            params.append(use_code)
        if rating_category:
            filters.append("rating_category = %s")
            params.append(rating_category)
        if market_value:
            filters.append("market_value = %s")
            params.append(market_value)
        if registered_extent:
            filters.append("registered_extent = %s")
            params.append(registered_extent)
        if suburb:
            filters.append("suburb = %s")
            params.append(suburb)
        if valuation_roll:
            filters.append("valuation_roll = %s")
            params.append(valuation_roll)

        if filters:
            select_query += " AND " + " AND ".join(filters)

        with conn.cursor() as cursor:
            cursor.execute(select_query, params)
            results = []
            for row in cursor.fetchall():
                results.append({
                    "rate_number": row[0],
                    "legal_description": row[1],
                    "address": row[2],
                    "first_owner": row[3],
                    "use_code": row[4],
                    "rating_category": row[5],
                    "market_value": row[6],
                    "registered_extent": row[7],
                    "suburb": row[8],
                    "valuation_roll": row[9]
                })
            return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving results: {e}")

openapi_schema = app.openapi()

@app.get("/openapi.json", include_in_schema=False)
def get_openapi_schema():
    return openapi_schema

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
