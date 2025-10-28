#!/usr/bin/env python3
"""
REST API Demo using Flask

Features:
- CRUD endpoints for a simple in-memory "books" resource
- JSON request/response with input validation
- Error handling with proper HTTP status codes
- Pagination and filtering examples
- Clear, commented code for learning REST fundamentals

Run locally:
    pip install flask
    python3 rest_api_demo.py
    # Visit http://127.0.0.1:5000/api/books
"""

from flask import Flask, request, jsonify, abort
from dataclasses import dataclass, asdict
from typing import List, Optional
import uuid

app = Flask(__name__)


@dataclass
class Book:
    id: str
    title: str
    author: str
    year: int
    tags: List[str]


# In-memory data store (for demo purposes only)
BOOKS: List[Book] = [
    Book(id=str(uuid.uuid4()), title="Clean Code", author="Robert C. Martin", year=2008, tags=["programming", "best-practices"]),
    Book(id=str(uuid.uuid4()), title="The Pragmatic Programmer", author="Andrew Hunt", year=1999, tags=["software", "craft"]),
]


def validate_book_payload(payload: dict, partial: bool = False) -> Optional[str]:
    required_fields = {"title": str, "author": str, "year": int, "tags": list}
    if not isinstance(payload, dict):
        return "Invalid JSON object"
    
    if not partial:
        for field, typ in required_fields.items():
            if field not in payload:
                return f"Missing field: {field}"
            if not isinstance(payload[field], typ):
                return f"Invalid type for {field}. Expected {typ.__name__}"
    else:
        # For partial updates (PATCH/PUT), only validate provided fields
        for field, value in payload.items():
            if field not in required_fields:
                return f"Unknown field: {field}"
            if not isinstance(value, required_fields[field]):
                return f"Invalid type for {field}. Expected {required_fields[field].__name__}"
    return None


@app.get("/api/books")
def list_books():
    """List books with optional filtering and pagination.
    Query params:
      - q: substring to match in title or author
      - page: page number (1-based)
      - limit: items per page
    """
    q = request.args.get("q", "").lower()
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))

    filtered = [b for b in BOOKS if q in b.title.lower() or q in b.author.lower()]
    start = (page - 1) * limit
    end = start + limit
    total = len(filtered)

    return jsonify({
        "page": page,
        "limit": limit,
        "total": total,
        "items": [asdict(b) for b in filtered[start:end]]
    })


@app.get("/api/books/<book_id>")
def get_book(book_id: str):
    for b in BOOKS:
        if b.id == book_id:
            return jsonify(asdict(b))
    abort(404, description="Book not found")


@app.post("/api/books")
def create_book():
    payload = request.get_json(silent=True)
    error = validate_book_payload(payload or {})
    if error:
        abort(400, description=error)

    book = Book(
        id=str(uuid.uuid4()),
        title=payload["title"],
        author=payload["author"],
        year=payload["year"],
        tags=payload["tags"],
    )
    BOOKS.append(book)
    return jsonify(asdict(book)), 201


@app.put("/api/books/<book_id>")
def update_book(book_id: str):
    payload = request.get_json(silent=True)
    error = validate_book_payload(payload or {}, partial=True)
    if error:
        abort(400, description=error)

    for i, b in enumerate(BOOKS):
        if b.id == book_id:
            # Update fields if provided
            BOOKS[i] = Book(
                id=b.id,
                title=payload.get("title", b.title),
                author=payload.get("author", b.author),
                year=payload.get("year", b.year),
                tags=payload.get("tags", b.tags),
            )
            return jsonify(asdict(BOOKS[i]))
    abort(404, description="Book not found")


@app.delete("/api/books/<book_id>")
def delete_book(book_id: str):
    for i, b in enumerate(BOOKS):
        if b.id == book_id:
            del BOOKS[i]
            return "", 204
    abort(404, description="Book not found")


@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e.description)), 400


@app.errorhandler(404)
def not_found(e):
    return jsonify(error=str(e.description)), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify(error="Internal server error"), 500


if __name__ == "__main__":
    # For development only; use a WSGI server (gunicorn/uwsgi) in production
    app.run(debug=True)
