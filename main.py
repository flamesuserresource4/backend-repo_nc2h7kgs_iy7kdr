import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import db, create_document, get_documents
from schemas import User, Product, Category, Order, Wishlist

app = FastAPI(title="Saaz International – Online Shopping API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"app": "Saaz International – Online Shopping API", "status": "ok"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set",
        "database_name": "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set",
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["connection_status"] = "Connected"
            try:
                response["collections"] = db.list_collection_names()[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"
    return response

# -----------------------------
# Minimal API for demo frontend
# -----------------------------

# Create category
@app.post("/api/categories")
def create_category(category: Category):
    cid = create_document("category", category)
    return {"id": cid}

# List categories
@app.get("/api/categories")
def list_categories(limit: Optional[int] = 50):
    cats = get_documents("category", {}, limit)
    for c in cats:
        c["_id"] = str(c.get("_id"))
    return cats

# Create product
@app.post("/api/products")
def create_product(product: Product):
    pid = create_document("product", product)
    return {"id": pid}

# List products with optional category filter
@app.get("/api/products")
def list_products(category: Optional[str] = None, limit: Optional[int] = 100):
    flt = {"category": category} if category else {}
    items = get_documents("product", flt, limit)
    for p in items:
        p["_id"] = str(p.get("_id"))
    return items

# Simple order creation
@app.post("/api/orders")
def create_order(order: Order):
    oid = create_document("order", order)
    return {"id": oid}

# List orders by user
@app.get("/api/orders")
def list_orders(user_id: Optional[str] = None, limit: Optional[int] = 50):
    flt = {"user_id": user_id} if user_id else {}
    items = get_documents("order", flt, limit)
    for o in items:
        o["_id"] = str(o.get("_id"))
    return items

# Wishlist endpoints
@app.post("/api/wishlist")
def add_to_wishlist(w: Wishlist):
    wid = create_document("wishlist", w)
    return {"id": wid}

@app.get("/api/wishlist")
def get_wishlist(user_id: str):
    items = get_documents("wishlist", {"user_id": user_id})
    for it in items:
        it["_id"] = str(it.get("_id"))
    return items


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
