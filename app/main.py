from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3
from datetime import datetime
from algorithms.knapsack import optimize_waste

# Initialize FastAPI
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Database setup
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS items (
    itemId TEXT PRIMARY KEY,
        name TEXT,
            width REAL, depth REAL, height REAL,
                mass REAL,
                    priority INTEGER,
                        expiryDate TEXT,
                            usageLimit INTEGER,
                                preferredZone TEXT
                                )
                                """)
                                conn.commit()

                                # Waste Management Endpoint
                                @app.post("/api/waste/return-plan")
                                async def generate_waste_plan(maxWeight: float):
                                    try:
                                            cursor.execute("""
                                                    SELECT itemId, mass, priority 
                                                            FROM items 
                                                                    WHERE expiryDate < DATE('now') OR usageLimit <= 0
                                                                            """)
                                                                                    waste_items = [
                                                                                                {"itemId": row[0], "mass": row[1], "priority": row[2]}
                                                                                                            for row in cursor.fetchall()
                                                                                                                    ]
                                                                                                                            
                                                                                                                                    if not waste_items:
                                                                                                                                                raise HTTPException(status_code=404, detail="No waste items found")
                                                                                                                                                        
                                                                                                                                                                result = optimize_waste(waste_items, maxWeight)
                                                                                                                                                                        
                                                                                                                                                                                return {
                                                                                                                                                                                            "success": True,
                                                                                                                                                                                                        "plan": {
                                                                                                                                                                                                                        "items_to_return": result["selected_items"],
                                                                                                                                                                                                                                        "total_weight_kg": result["total_weight"],
                                                                                                                                                                                                                                                        "priority_score": result["total_priority"]
                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                                        except Exception as e:
                                                                                                                                                                                                                                                                                                raise HTTPException(status_code=500, detail=str(e))

                                                                                                                                                                                                                                                                                                # UI Endpoint
                                                                                                                                                                                                                                                                                                @app.get("/", response_class=HTMLResponse)
                                                                                                                                                                                                                                                                                                async def serve_ui(request: Request):
                                                                                                                                                                                                                                                                                                    return templates.TemplateResponse("index.html", {"request": request})

                                                                                                                                                                                                                                                                                                    if __name__ == "__main__":
                                                                                                                                                                                                                                                                                                        import uvicorn
                                                                                                                                                                                                                                                                                                            uvicorn.run(app, host="0.0.0.0", port=8000)
                                                                                                                                                                                                                                    