"""
Logs endpoint router.
"""

from fastapi import APIRouter, Depends, Query, HTTPException, status
from fastapi.responses import Response, StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import Optional, List
from datetime import datetime
import csv
import io
import json

from app.database import get_db
from app.models import RequestLog, Decision, RiskType
from app.schemas import LogFilterSchema
from app.auth import get_current_admin_user

router = APIRouter()


@router.get("/v1/logs")
async def get_logs(
    type: Optional[str] = Query(None, description="Filter by risk type (PII, PHI, PROMPT_INJECTION)"),
    severity: Optional[str] = Query(None, description="Filter by severity (high, medium, low)"),
    date_from: Optional[str] = Query(None, description="Start date (ISO format)"),
    date_to: Optional[str] = Query(None, description="End date (ISO format)"),
    limit: int = Query(50, ge=1, le=1000, description="Number of logs to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    format: str = Query("json", pattern="^(json|csv)$", description="Export format"),
    db: Session = Depends(get_db),
    # current_user = Depends(get_current_admin_user)  # Temporarily disabled for testing
):
    """
    Retrieve firewall logs with filtering and pagination.
    
    - **type**: Filter by risk type
    - **severity**: Filter by severity level
    - **date_from**: Start date for filtering
    - **date_to**: End date for filtering
    - **limit**: Number of logs to return (1-1000)
    - **offset**: Pagination offset
    - **format**: Export format (json or csv)
    
    Returns filtered and paginated logs.
    """
    query = db.query(RequestLog)
    
    # Apply filters
    if type:
        try:
            risk_type = RiskType(type)
            query = query.filter(RequestLog.risks.contains([{"type": risk_type.value}]))
        except ValueError:
            pass
    
    if severity:
        query = query.filter(RequestLog.risks.contains([{"severity": severity}]))
    
    if date_from:
        try:
            date_from_obj = datetime.fromisoformat(date_from.replace('Z', '+00:00'))
            query = query.filter(RequestLog.timestamp >= date_from_obj)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid date_from format. Use ISO format."
            )
    
    if date_to:
        try:
            date_to_obj = datetime.fromisoformat(date_to.replace('Z', '+00:00'))
            query = query.filter(RequestLog.timestamp <= date_to_obj)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid date_to format. Use ISO format."
            )
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    logs = query.order_by(RequestLog.timestamp.desc()).offset(offset).limit(limit).all()
    
    # Format logs
    log_data = [
        {
            "id": log.id,
            "request_id": log.request_id,
            "timestamp": log.timestamp.isoformat() if log.timestamp else None,
            "original_prompt": log.original_prompt,
            "modified_prompt": log.modified_prompt,
            "original_response": log.original_response,
            "modified_response": log.modified_response,
            "decision": log.decision.value if log.decision else None,
            "risks": log.risks if isinstance(log.risks, list) else [],
            "metadata": log.request_metadata if isinstance(log.request_metadata, dict) else {}
        }
        for log in logs
    ]
    
    # Handle export formats
    if format == "csv":
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=[
            "id", "request_id", "timestamp", "decision", "risk_count"
        ])
        writer.writeheader()
        for log in log_data:
            writer.writerow({
                "id": log["id"],
                "request_id": log["request_id"],
                "timestamp": log["timestamp"],
                "decision": log["decision"],
                "risk_count": len(log["risks"])
            })
        output.seek(0)
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=logs.csv"}
        )
    
    # Default JSON response
    return {
        "logs": log_data,
        "total": total,
        "limit": limit,
        "offset": offset,
        "has_more": (offset + limit) < total
    }

