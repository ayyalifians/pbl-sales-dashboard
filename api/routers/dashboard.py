# api/routers/dashboard.py
from fastapi import APIRouter, HTTPException, Query
from database.connection import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import Depends
from typing import Optional

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

# ════════════════════════════════
#   ENDPOINT: SUMMARY (KPI Cards)
# ════════════════════════════════

@router.get(
    "/summary",
    summary="Get Dashboard Summary",
    description="Ambil ringkasan KPI: total sales, profit, orders, customers"
)
async def get_summary(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("""
            SELECT
                ROUND(SUM(o.sales)::numeric, 2)  AS total_sales,
                ROUND(SUM(o.profit)::numeric, 2) AS total_profit,
                COUNT(*)                          AS total_orders,
                COUNT(DISTINCT o.customer_id)     AS total_customers
            FROM orders o
        """)).fetchone()

        return {
            "total_sales"    : float(result.total_sales),
            "total_profit"   : float(result.total_profit),
            "total_orders"   : int(result.total_orders),
            "total_customers": int(result.total_customers)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error summary: {str(e)}")


# ════════════════════════════════
#   ENDPOINT: SALES MONTHLY CHART
# ════════════════════════════════

@router.get(
    "/sales-monthly",
    summary="Get Monthly Sales Chart Data",
    description="Data penjualan bulanan untuk line chart dashboard"
)
async def get_sales_monthly(
    category: Optional[str] = Query(None),
    year    : Optional[int] = Query(None),
    db      : Session = Depends(get_db)
):
    try:
        base_query = """
            SELECT
                year,
                month,
                category,
                ROUND(total_sales::numeric, 2)  AS total_sales,
                ROUND(total_profit::numeric, 2) AS total_profit,
                num_orders
            FROM ts_sales_monthly
            WHERE 1=1
        """
        params = {}

        if category:
            base_query        += " AND category = :category"
            params['category'] = category

        if year:
            base_query    += " AND year = :year"
            params['year'] = year

        base_query += " ORDER BY year ASC, month ASC"

        result = db.execute(text(base_query), params).fetchall()
        data   = [dict(row._mapping) for row in result]

        return {
            "total_records": len(data),
            "filter"       : {
                "category": category or "All",
                "year"    : year or "All"
            },
            "data": data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sales monthly: {str(e)}")


# ════════════════════════════════
#   ENDPOINT: SALES BY CATEGORY
# ════════════════════════════════

@router.get(
    "/sales-by-category",
    summary="Get Sales By Category",
    description="Total penjualan per kategori untuk pie/bar chart"
)
async def get_sales_by_category(
    year: Optional[int] = Query(None),
    db  : Session = Depends(get_db)
):
    try:
        base_query = """
            SELECT
                p.category,
                ROUND(SUM(o.sales)::numeric, 2)  AS total_sales,
                ROUND(SUM(o.profit)::numeric, 2) AS total_profit,
                COUNT(*)                          AS total_orders
            FROM orders o
            JOIN products p ON o.product_id = p.product_id
            WHERE 1=1
        """
        params = {}

        if year:
            base_query    += " AND EXTRACT(YEAR FROM o.order_date) = :year"
            params['year'] = year

        base_query += " GROUP BY p.category ORDER BY total_sales DESC"

        result = db.execute(text(base_query), params).fetchall()
        data   = [dict(row._mapping) for row in result]

        return {
            "filter": {"year": year or "All"},
            "data"  : data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error by category: {str(e)}")


# ════════════════════════════════
#   ENDPOINT: TOP PRODUCTS
# ════════════════════════════════

@router.get(
    "/top-products",
    summary="Get Top Products",
    description="Produk dengan penjualan tertinggi"
)
async def get_top_products(
    limit   : int            = Query(10),
    category: Optional[str] = Query(None),
    db      : Session = Depends(get_db)
):
    try:
        base_query = """
            SELECT
                p.product_name,
                p.category,
                p.sub_category,
                ROUND(SUM(o.sales)::numeric, 2)  AS total_sales,
                ROUND(SUM(o.profit)::numeric, 2) AS total_profit,
                COUNT(*)                          AS total_orders
            FROM orders o
            JOIN products p ON o.product_id = p.product_id
            WHERE 1=1
        """
        params = {"limit": limit}

        if category:
            base_query        += " AND p.category = :category"
            params['category'] = category

        base_query += """
            GROUP BY p.product_name, p.category, p.sub_category
            ORDER BY total_sales DESC
            LIMIT :limit
        """

        result = db.execute(text(base_query), params).fetchall()
        data   = [dict(row._mapping) for row in result]

        return {
            "total_records": len(data),
            "data"         : data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error top products: {str(e)}")