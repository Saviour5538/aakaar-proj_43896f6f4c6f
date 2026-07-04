from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database.models import Document
from database.config import get_db
from backend.services.auth_service import get_current_user

router = APIRouter(prefix="/api/documents")

class DocumentResponse(BaseModel):
    id: UUID
    user_id: UUID
    filename: str
    status: str
    chunk_count: int
    created_at: str

    class Config:
        orm_mode = True


@router.post(
    "/upload",
    operation_id="uploadDocument",
    status_code=status.HTTP_201_CREATED,
    response_model=None,
)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        # Placeholder for actual upload logic
        document = Document(
            user_id=current_user["id"],
            filename=file.filename,
            status="uploaded",
            chunk_count=0,
            created_at="now",  # Replace with actual timestamp logic
        )
        db.add(document)
        db.commit()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload document: {str(e)}",
        )


@router.get(
    "/",
    operation_id="listDocuments",
    response_model=List[DocumentResponse],
)
def list_documents(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        documents = db.query(Document).filter(Document.user_id == current_user["id"]).all()
        return documents
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list documents: {str(e)}",
        )


@router.delete(
    "/{id}",
    operation_id="deleteDocument",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
def delete_document(
    id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        document = db.query(Document).filter(Document.id == id, Document.user_id == current_user["id"]).first()
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found",
            )
        db.delete(document)
        db.commit()
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete document: {str(e)}",
        )