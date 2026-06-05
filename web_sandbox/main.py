#!/usr/bin/env python3
"""
theZoo Web Sandbox - FastAPI Web Interface for theZoo Malware Repository

This module provides a web-based interface for browsing and interacting with
the theZoo malware database. It maintains all safety features of the original
application while providing a modern, accessible web interface.

IMPORTANT: This is designed for use in isolated sandbox environments only.
"""

import sys
import os
from typing import List, Optional, Dict, Any
from contextlib import asynccontextmanager

# Add parent directory to path to import theZoo modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Request, HTTPException, Query, Form
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import uvicorn

from imports.db_handler import DBHandler
from imports.update_handler import Updater
from imports import globals as zoo_globals
from imports import manysearches

# Application metadata
__version__ = "0.1.0"
__appname__ = "theZoo Web Sandbox"

# Templates directory - configure Jinja2 to disable caching for compatibility
from jinja2 import FileSystemLoader, Environment

# Create a custom Jinja2 environment with no caching
jinja_env = Environment(
    loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")),
    autoescape=True,
    cache_size=0  # Disable caching
)
templates = Jinja2Templates(env=jinja_env)

# Global database connection
db: Optional[DBHandler] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan - initialize and cleanup resources."""
    global db
    # Startup: Initialize database connection
    db = DBHandler()
    print(f"[+] theZoo Web Sandbox v{__version__} started")
    print(f"[+] Connected to malware database")
    yield
    # Shutdown: Close database connection
    if db:
        db.close_connection()
    print(f"[-] Database connection closed")


# Create FastAPI application
app = FastAPI(
    title=__appname__,
    description="Web-based sandbox interface for theZoo malware repository",
    version=__version__,
    lifespan=lifespan
)

# Mount static files directory if it exists
static_path = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")


# ============================================================================
# Helper Functions
# ============================================================================

def get_db() -> DBHandler:
    """Get database handler instance."""
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection not available")
    return db


def search_malware(query: str) -> List[Dict[str, Any]]:
    """
    Search malware database using theZoo's search functionality.
    
    Args:
        query: Search query string (can include type, platform, language, etc.)
    
    Returns:
        List of matching malware entries
    """
    if not query or not query.strip():
        return []
    
    # Parse query into arguments (similar to terminal_handler)
    args = query.strip().split()
    
    if not args:
        return []
    
    # Use theZoo's search mechanism
    searcher = manysearches.MuchSearch()
    hits = searcher.sort(args)
    
    # Convert results to list of dicts
    results = []
    for row in searcher.ar:
        results.append({
            'id': row[0],
            'type': row[1],
            'language': row[2],
            'architecture': row[3],
            'platform': row[4],
            'name': row[5]
        })
    
    return results


# ============================================================================
# Web Routes (HTML Pages)
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page - Dashboard with overview and warnings."""
    db = get_db()
    
    # Get database statistics
    stats = db.get_connection_info()
    
    # Get some sample data for the dashboard
    try:
        recent_malwares = db.get_partial_details()[-10:]  # Last 10 entries
    except:
        recent_malwares = []
    
    return templates.TemplateResponse("home.html", {
        "request": request,
        "stats": stats,
        "recent_malwares": recent_malwares,
        "version": __version__,
        "zoo_version": zoo_globals.vars.version,
        "page_title": "Dashboard"
    })


@app.get("/browse", response_class=HTMLResponse)
async def browse_malwares(
    request: Request,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=10, le=200),
    filter_type: Optional[str] = Query(None),
    filter_platform: Optional[str] = Query(None),
    filter_arch: Optional[str] = Query(None),
    filter_lang: Optional[str] = Query(None),
):
    """Browse malware database with optional filters."""
    db = get_db()
    
    # Build query based on filters
    where_clauses = []
    params = []
    
    if filter_type:
        where_clauses.append("TYPE LIKE ?")
        params.append(f"%{filter_type}%")
    if filter_platform:
        where_clauses.append("PLATFORM LIKE ?")
        params.append(f"%{filter_platform}%")
    if filter_arch:
        where_clauses.append("ARCHITECTURE LIKE ?")
        params.append(f"%{filter_arch}%")
    if filter_lang:
        where_clauses.append("LANGUAGE LIKE ?")
        params.append(f"%{filter_lang}%")
    
    where_sql = ""
    if where_clauses:
        where_sql = "WHERE " + " AND ".join(where_clauses)
    
    # Get total count
    count_query = f"SELECT COUNT(*) FROM Malwares {where_sql}"
    total_count = db.query(count_query, params)[0][0] if params else db.query("SELECT COUNT(*) FROM Malwares")[0][0]
    
    # Get paginated results
    offset = (page - 1) * per_page
    query = f"""
        SELECT ID, TYPE, LANGUAGE, ARCHITECTURE, PLATFORM, NAME 
        FROM Malwares {where_sql}
        ORDER BY ID
        LIMIT ? OFFSET ?
    """
    query_params = params + [per_page, offset]
    malwares = db.query(query, query_params)
    
    # Get available filter options
    types = db.query("SELECT DISTINCT TYPE FROM Malwares WHERE TYPE IS NOT NULL AND TYPE != '' ORDER BY TYPE")
    platforms = db.query("SELECT DISTINCT PLATFORM FROM Malwares WHERE PLATFORM IS NOT NULL AND PLATFORM != '' ORDER BY PLATFORM")
    architectures = db.query("SELECT DISTINCT ARCHITECTURE FROM Malwares WHERE ARCHITECTURE IS NOT NULL AND ARCHITECTURE != '' ORDER BY ARCHITECTURE")
    languages = db.query("SELECT DISTINCT LANGUAGE FROM Malwares WHERE LANGUAGE IS NOT NULL AND LANGUAGE != '' ORDER BY LANGUAGE")
    
    return templates.TemplateResponse("browse.html", {
        "request": request,
        "malwares": malwares,
        "page": page,
        "per_page": per_page,
        "total_count": total_count,
        "total_pages": (total_count + per_page - 1) // per_page,
        "filter_type": filter_type,
        "filter_platform": filter_platform,
        "filter_arch": filter_arch,
        "filter_lang": filter_lang,
        "types": [t[0] for t in types],
        "platforms": [p[0] for p in platforms],
        "architectures": [a[0] for a in architectures],
        "languages": [l[0] for l in languages],
        "page_title": "Browse Malwares"
    })


@app.get("/search", response_class=HTMLResponse)
async def search_page(request: Request, q: Optional[str] = Query(None)):
    """Search page with results."""
    results = []
    query_text = q or ""
    
    if query_text:
        results = search_malware(query_text)
    
    return templates.TemplateResponse("search.html", {
        "request": request,
        "results": results,
        "query": query_text,
        "page_title": "Search"
    })


@app.get("/malware/{mal_id}", response_class=HTMLResponse)
async def malware_details(request: Request, mal_id: int):
    """View detailed information about a specific malware."""
    db = get_db()
    
    # Get malware info
    mal_info = db.get_mal_info(mal_id)
    
    if not mal_info:
        raise HTTPException(status_code=404, detail="Malware not found")
    
    # Parse the info tuple
    info = mal_info[0]
    malware = {
        'id': mal_id,
        'type': info[0],
        'name': info[1],
        'version': info[2],
        'author': info[3],
        'language': info[4],
        'date': info[5],
        'architecture': info[6],
        'platform': info[7],
        'tags': info[8]
    }
    
    # Get location for download
    try:
        location_query = db.query("SELECT LOCATION FROM Malwares WHERE ID=?", mal_id)
        location = location_query[0][0] if location_query else None
    except:
        location = None
    
    return templates.TemplateResponse("malware_detail.html", {
        "request": request,
        "malware": malware,
        "location": location,
        "page_title": f"Malware: {malware['name']}"
    })


@app.get("/download/{mal_id}", response_class=HTMLResponse)
async def download_page(request: Request, mal_id: int):
    """Download page with safety warnings."""
    db = get_db()
    
    # Get malware name
    mal_info = db.get_mal_info(mal_id)
    if not mal_info:
        raise HTTPException(status_code=404, detail="Malware not found")
    
    malware_name = mal_info[0][1]
    
    # Get location
    try:
        location_query = db.query("SELECT LOCATION FROM Malwares WHERE ID=?", mal_id)
        location = location_query[0][0] if location_query else None
    except:
        location = None
    
    return templates.TemplateResponse("download.html", {
        "request": request,
        "mal_id": mal_id,
        "malware_name": malware_name,
        "location": location,
        "page_title": f"Download: {malware_name}"
    })


@app.get("/documentation", response_class=HTMLResponse)
async def documentation(request: Request):
    """Documentation page with links to theZoo documentation."""
    return templates.TemplateResponse("documentation.html", {
        "request": request,
        "page_title": "Documentation",
        "zoo_version": zoo_globals.vars.version,
        "github_url": zoo_globals.vars.github_add,
        "license": zoo_globals.vars.licensev
    })


@app.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    """About page with license and version information."""
    return templates.TemplateResponse("about.html", {
        "request": request,
        "page_title": "About",
        "version": __version__,
        "zoo_version": zoo_globals.vars.version,
        "authors": zoo_globals.vars.authors,
        "license": zoo_globals.vars.licensev,
        "github_url": zoo_globals.vars.github_add,
        "full_license": zoo_globals.vars.fulllicense
    })


# ============================================================================
# API Routes (JSON)
# ============================================================================

@app.get("/api/stats")
async def api_stats():
    """Get database statistics."""
    db = get_db()
    stats = db.get_connection_info()
    return JSONResponse(content={
        "database_path": stats['database_path'],
        "malware_count": stats['malware_count'],
        "connection_active": stats['connection_active'],
        "web_sandbox_version": __version__,
        "thezoo_version": zoo_globals.vars.version
    })


@app.get("/api/malwares")
async def api_list_malwares(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=10, le=500)
):
    """List malware samples with pagination."""
    db = get_db()
    
    # Get total count
    total_count = db.query("SELECT COUNT(*) FROM Malwares")[0][0]
    
    # Get paginated results
    offset = (page - 1) * per_page
    malwares = db.get_partial_details()
    
    # Apply pagination
    paginated = malwares[offset:offset + per_page]
    
    return JSONResponse(content={
        "total": total_count,
        "page": page,
        "per_page": per_page,
        "total_pages": (total_count + per_page - 1) // per_page,
        "malwares": [
            {
                "id": m[0],
                "type": m[1],
                "language": m[2],
                "architecture": m[3],
                "platform": m[4],
                "name": m[5]
            } for m in paginated
        ]
    })


@app.get("/api/malwares/{mal_id}")
async def api_get_malware(mal_id: int):
    """Get detailed information about a specific malware."""
    db = get_db()
    
    mal_info = db.get_mal_info(mal_id)
    if not mal_info:
        raise HTTPException(status_code=404, detail="Malware not found")
    
    info = mal_info[0]
    return JSONResponse(content={
        "id": mal_id,
        "type": info[0],
        "name": info[1],
        "version": info[2],
        "author": info[3],
        "language": info[4],
        "date": info[5],
        "architecture": info[6],
        "platform": info[7],
        "tags": info[8]
    })


@app.get("/api/malwares/search")
async def api_search_malwares(q: str = Query(..., min_length=1)):
    """Search malware database."""
    results = search_malware(q)
    return JSONResponse(content={
        "query": q,
        "count": len(results),
        "results": results
    })


@app.post("/api/update-db")
async def api_update_db():
    """Update the malware database."""
    try:
        updater = Updater()
        current_version = updater.get_maldb_ver()
        
        # This will update the database
        # Note: This is a simplified version - in production you might want
        # to handle this asynchronously
        updater.update_db(current_version)
        
        return JSONResponse(content={
            "status": "success",
            "message": "Database updated successfully"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Error Handlers
# ============================================================================

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Handle 404 errors."""
    return templates.TemplateResponse("error.html", {
        "request": request,
        "error_code": 404,
        "error_message": "Page not found",
        "page_title": "404 - Not Found"
    }, status_code=404)


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    """Handle 500 errors."""
    return templates.TemplateResponse("error.html", {
        "request": request,
        "error_code": 500,
        "error_message": "Internal server error",
        "page_title": "500 - Internal Error"
    }, status_code=500)


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  theZoo Web Sandbox")
    print("  A web-based interface for theZoo malware repository")
    print("=" * 60)
    print()
    print("⚠️  SECURITY WARNING ⚠️")
    print("This sandbox should ONLY be run in an isolated environment!")
    print("The theZoo repository contains LIVE MALWARE that can:")
    print("  - Infect your system")
    print("  - Spread to other machines")
    print("  - Cause permanent damage")
    print()
    print("Always use proper safety precautions!")
    print()
    
    uvicorn.run(
        app,
        host="127.0.0.1",  # Bind to localhost for security
        port=8000,
        reload=True
    )