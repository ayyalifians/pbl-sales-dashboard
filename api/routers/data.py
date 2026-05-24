# api/routers/data.py
from fastapi import APIRouter, HTTPException, Query
from database.connection import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
import pandas as pd

router = APIRouter(
    prefix="/data",
    tags=["Data"]
)

# ════════════════════════════════
#   ENDPOINT: SALES HISTORY
# ════════════════════════════════

@router.get(
    "/sales/history",
    summary="Get Sales History",
    description="Ambil data historis penjualan dari database"
)
async def get_sales_history(
    category: str = Query(None, description="Filter by category"),
    year    : int = Query(None, description="Filter by year"),
    db      : Session = Depends(get_db)
):
    try:
        query = """
            SELECT
                o.order_date,
                p.category,
                p.sub_category,
                SUM(o.sales)    AS total_sales,
                SUM(o.profit)   AS total_profit,
                COUNT(*)        AS total_orders
            FROM orders o
            JOIN products p ON o.product_id = p.product_id
            WHERE 1=1
        """
        params = {}

        if category:
            query  += " AND p.category = :category"
            params['category'] = category

        if year:
            query  += " AND EXTRACT(YEAR FROM o.order_date) = :year"
            params['year'] = year

        query += " GROUP BY o.order_date, p.category, p.sub_category ORDER BY o.order_date"

        result = db.execute(query, params).fetchall()
        data   = [dict(row._mapping) for row in result]

        return {
            "total_records": len(data),
            "category"     : category or "All",
            "year"         : year or "All",
            "data"         : data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# ════════════════════════════════
#   ENDPOINT: SAVED PREDICTIONS
# ════════════════════════════════

@router.get(
    "/predictions/saved",
    summary="Get Saved Predictions",
    description="Ambil hasil prediksi yang sudah tersimpan di database"
)
async def get_saved_predictions(
    category: str = Query(None, description="Filter by category"),
    db      : Session = Depends(get_db)
):
    try:
        query = "SELECT * FROM ml_predictions WHERE 1=1"
        params = {}

        if category:
            query        += " AND category = :category"
            params['category'] = category

        query += " ORDER BY created_at DESC"

        result = db.execute(query, params).fetchall()
        data   = [dict(row._mapping) for row in result]

        return {
            "total_records": len(data),
            "data"         : data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")