from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import select, delete
from database.db import engine

from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse

from typing import List, Optional
from schemas.dictionary_shemas import TermShema
from database.models import Term

dictionary_router = APIRouter()

@dictionary_router.get('/dictionary', response_model=List[TermShema])
async def get_dictionary() -> JSONResponse:
    async with AsyncSession(engine) as session:
        terms = await session.execute(
            select(Term)
        )
        terms = terms.scalars()
        terms = [{x.name: getattr(scalar, x.name) for x in scalar.__table__.columns} for scalar in terms]
    return JSONResponse(terms, status_code=status.HTTP_200_OK)

@dictionary_router.post('/term', response_model=TermShema)
async def post_term(term: TermShema) -> JSONResponse:
    async with AsyncSession(engine) as session:
        partition = Term(**dict(term))
        session.add(partition)
        try:
            await session.commit()
        except:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)
        partition = await session.execute(
            select(Term).\
            where(Term.term == term.term)
        )
        partition = partition.scalar_one()
        res = TermShema(**{x.name: getattr(partition, x.name) for x in partition.__table__.columns})
        
    return JSONResponse(dict(res), status_code=status.HTTP_200_OK)

@dictionary_router.put('/term', response_model=TermShema)
async def put_term(term: TermShema) -> JSONResponse:
    async with AsyncSession(engine) as session:
        if term.id != None:
            partition = await session.execute(
                select(Term).\
                where(Term.id == term.id)
            )
        elif term.term != None:
            partition = await session.execute(
                select(Term).\
                where(Term.term == term.term)
            )
        else:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        partition = partition.scalar_one_or_none()
        if partition == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        partition.term = term.term
        partition.definition = term.definition
        partition.case_sensitive = term.case_sensitive
        res = TermShema(**{x.name: getattr(partition, x.name) for x in partition.__table__.columns})
        await session.commit()
    return JSONResponse(dict(res), status_code=status.HTTP_200_OK)

@dictionary_router.get('/term', response_model=TermShema)
async def get_term(id: Optional[int]=None, term: Optional[str]=None) -> JSONResponse:
    async with AsyncSession(engine) as session:
        if id != None:
            partition = await session.execute(
                select(Term.id, Term.term, Term.definition, Term.case_sensitive).\
                where(Term.id == id)
            )
        elif term != None:
            partition = await session.execute(
                select(Term.id, Term.term, Term.definition, Term.case_sensitive).\
                where(Term.term == term)
            )
        else:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        partition = partition.first()
        if partition == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        partition = TermShema(**partition._mapping)
    return JSONResponse(dict(partition), status_code=status.HTTP_200_OK)

@dictionary_router.delete('/term')
async def delete_term(id: Optional[int]=None, term: Optional[str]=None) -> JSONResponse:
    async with AsyncSession(engine) as session:
        if id != None:
            await session.execute(
                delete(Term).\
                where(Term.id == id)
            )
        elif term != None:
            await session.execute(
                delete(Term).\
                where(Term.term == term)
            )
        else:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        try:
            await session.commit()
        except:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse({}, status_code=status.HTTP_200_OK)