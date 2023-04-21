from datetime import datetime
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload, joinedload, contains_eager

from app.core.logger import logger
from app.deps.db import get_async_session
from app.models.company import Company, Qliq, Qoil
from app.schemas.companies import Company as CompanySchema, CompanyTotal
from app.schemas.companies import CompanyCreate

from app.services.company_service import MetricsService, CompanyService
from app.services.xlsx_parse_service import XlsxParseService


router = APIRouter(prefix="/companies")


@router.post("", response_model=CompanySchema, status_code=201)
async def create_company(
        company_in: CompanyCreate,
        session: AsyncSession = Depends(get_async_session),
):
    company = Company(**company_in.dict())
    session.add(company)
    await session.commit()
    return company


@router.get("", response_model=List[CompanySchema], status_code=200)
async def get_companies_list(
        session: AsyncSession = Depends(get_async_session),
):
    companies = (
        (await session.execute(select(Company))).scalars().all()
    )
    return companies


@router.get("/total", response_model=List[CompanyTotal], status_code=200)
async def get_companies_total(
        date: str,
        session: AsyncSession = Depends(get_async_session),
):
    date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    logger.info(date_obj)
    #
    service = CompanyService(Company)
    companies = await service.get_total_by_date(session, date_obj)
    return companies


@router.get("/qliqs", status_code=200)
async def get_qliqs(
    session: AsyncSession = Depends(get_async_session),
    service = Depends(MetricsService)
) -> Any:
    qliqs = await service.get_metric_list(session, Qliq)
    return qliqs


@router.get("/qoils", status_code=200)
async def get_qoils(
    session: AsyncSession = Depends(get_async_session),
    service = Depends(MetricsService)
) -> Any:
    qoils = await service.get_metric_list(session, Qoil)
    return qoils


@router.post("/upload", status_code=200)
async def upload_file(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_async_session),
    service = Depends(MetricsService)
):
    bytz = await file.read()

    # if huge file need to chunk it and process concurrent
    # in terms of development speed we let this go sync
    parse_service = XlsxParseService(bytz)
    parse_service.parse()

    logger.info(parse_service.fact_qliq)
    logger.info(parse_service.forecast_qliq)

    await service.load_metrics(
        session, Qliq, parse_service.fact_qliq, parse_service.forecast_qliq
    )
    await service.load_metrics(
        session, Qoil, parse_service.fact_qoil, parse_service.forecast_qoil
    )
    await session.commit()

    return {'upload': 'OK'}