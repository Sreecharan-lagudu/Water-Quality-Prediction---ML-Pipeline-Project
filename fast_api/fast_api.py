# Importing required libraries
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError, Field
from typing import Optional, List, Dict, Any
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, date
import logging
import json
import warnings
import traceback

warnings.filterwarnings("ignore")

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# Database Configuration
class DatabaseConfig:
    DBNAME = "aqua"
    USER = "postgres"
    PASSWORD = "Charanrocks@2597"
    HOST = "localhost"
    PORT = "5432"

# Defining prediction class
class Prediction(BaseModel):
    ph: float
    iron: float
    nitrate: float
    chloride: float
    lead: float
    zinc: float
    color: str
    turbidity: float
    fluoride: float
    copper: float
    odor: str
    sulfate: float
    conductivity: float
    chlorine: float
    manganese: float
    tds: float
    source: str
    water_temp: float
    air_temp: float
    month: int
    day: int
    time_of_day: str
    prediction: int


# Database Connection Dependency
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",  # Force IPv4
            user=DatabaseConfig.USER,
            password=DatabaseConfig.PASSWORD,
            dbname=DatabaseConfig.DBNAME,
            connect_timeout=3,
        )
        logger.info("Successfully connected to database")
        return conn
    except psycopg2.OperationalError as e:
        logger.error(f"Connection failed: {e}")
        raise HTTPException(status_code=503, detail=f"Database connection failed: {e}")


# FastAPI App
app = FastAPI(title="Water Quality Prediction API")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Enhancing Validation Error Handler
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    """
    Provide extremely detailed validation error messages
    """
    # Log the full request body for debugging
    try:
        body = await request.json()
        logger.error(f"Request Body: {body}")
    except Exception as e:
        logger.error(f"Could not read request body: {e}")

    # Detailed error logging
    logger.error("Validation Errors:")
    for error in exc.errors():
        logger.error(f"Location: {error.get('loc')}")
        logger.error(f"Type: {error.get('type')}")
        logger.error(f"Message: {error.get('msg')}")
        logger.error("---")

    return JSONResponse(
        status_code=422, content={"detail": "Validation Error", "errors": exc.errors()}
    )

# Saving the predictions
@app.post("/save_predictions/")
def save_predictions(
    predictions: List[Prediction],  # Accept a list of Prediction objects
    conn: psycopg2.extensions.connection = Depends(get_db_connection),
):
    """
    Save a list of predictions with extensive logging and error handling
    """
    try:
        # Log incoming predictions
        logger.info(f"Received {len(predictions)} predictions")

        with conn.cursor() as cur:
            # Query for bulk insertion
            query = """
                INSERT INTO predictions (
                    ph, iron, nitrate, chloride, lead, zinc, color, turbidity,
                    fluoride, copper, odor, sulfate, conductivity, chlorine,
                    manganese, tds, source, water_temp, air_temp, month, day,
                    time_of_day, prediction, timestamp
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP
                )
            """

            # Data for bulk insertion
            data = [
                (
                    pred.ph,
                    pred.iron,
                    pred.nitrate,
                    pred.chloride,
                    pred.lead,
                    pred.zinc,
                    pred.color,
                    pred.turbidity,
                    pred.fluoride,
                    pred.copper,
                    pred.odor,
                    pred.sulfate,
                    pred.conductivity,
                    pred.chlorine,
                    pred.manganese,
                    pred.tds,
                    pred.source,
                    pred.water_temp,
                    pred.air_temp,
                    pred.month,
                    pred.day,
                    pred.time_of_day,
                    pred.prediction,
                )
                for pred in predictions
            ]

            # Executing the bulk insertion
            cur.executemany(query, data)
            conn.commit()

            logger.info(f"Successfully saved {len(predictions)} predictions")
            return {"message": f"{len(predictions)} predictions saved successfully"}

    except Exception as e:
        traceback.print_exc()
        logger.error(f"Unexpected error saving predictions: {e}")
        conn.rollback()  # Rollback in case of error
        raise HTTPException(
            status_code=500, detail=f"Error saving predictions: {str(e)}"
        )
# Function for fetching the predictions
@app.get("/get_predictions/", response_model=List[Dict[str, Any]])
def get_predictions(
    params: Dict[str, Optional[date]] = Depends(lambda: {}),
    conn: psycopg2.extensions.connection = Depends(get_db_connection),
):
    """
    Fetch predictions with optional date filtering

    - Accepts a dictionary `params` with `start_date` and `end_date`
    - Returns results as a list of dictionaries
    - Handles empty result sets
    """
    start_date = params.get("start_date")
    end_date = params.get("end_date")

    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            if start_date and end_date:
                query = """
                    SELECT * FROM predictions 
                    WHERE timestamp BETWEEN %s AND %s 
                    ORDER BY timestamp DESC
                """
                cur.execute(query, (start_date, end_date))
            else:
                query = "SELECT * FROM predictions ORDER BY timestamp DESC LIMIT 1000"
                cur.execute(query)

            results = cur.fetchall()

            if not results:
                return []

            # Convering the results from DictCursor to a list of dictionaries
            predictions = [dict(row) for row in results]

            logger.info(f"Retrieved {len(predictions)} prediction records")
            return predictions
    except psycopg2.Error as e:
        logger.error(f"Database query error: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# Debugging Endpoint to Check Incoming Payload
@app.post("/debug_prediction/")
async def debug_prediction(request: Request):
    """
    Endpoint to log and return the exact payload received
    """
    try:
        body = await request.json()
        logger.debug(f"Debug Payload: {body}")
        return {"received_payload": body}
    except Exception as e:
        logger.error(f"Error in debug endpoint: {e}")
        return {"error": str(e)}


# Health Check Endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}
