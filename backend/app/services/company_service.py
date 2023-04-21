import datetime
import random
import typing as t

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import contains_eager

from app.core.logger import logger
from app.models.company import Company, Qliq, Qoil


class BaseService:

    def __init__(self, model):
        self.model = model

    async def create(self, session, obj_in):
        obj = self.model(**obj_in.dict())
        session.add(obj)
        await session.commit()
        return obj

    async def get_by_id(self):
        ...

    async def get_list(self):
        ...


class CompanyService(BaseService):

    async def get_by_title(self, session, title):
        stmt = select(self.model).where(self.model.title == title)
        company = (await session.execute(stmt)).scalars().first()
        logger.info(company)
        return company

    async def get_total_by_date(self, session, date_obj):
        companies = (
            (
                await session.execute(
                    select(Company)
                    .join(Company.qliqs)
                    .join(Company.qoils)
                    .options(
                        contains_eager(Company.qliqs),
                        contains_eager(Company.qoils),
                    )
                    .where(Qliq.metric_date == date_obj)
                    .where(Qoil.metric_date == date_obj)
                )
            )
            .unique().scalars().all()
        )
        return companies

class MetricsService:

    def generate_date(self, day):
        """within a month"""
        start_date = datetime.datetime.now()
        end_date = start_date - datetime.timedelta(day)
        return end_date

    async def get_metric_list(self, session, model):
        metric_list = (
            (await session.execute(select(model))).scalars().all()
        )
        return metric_list

    async def load_metrics(self, session, model, fact, forecast):
        """load metrics to db, query optimisation skipped by now"""
        day = 1

        for fact, forecast in zip(fact, forecast):
            stmt = select(Company).where(Company.title == fact['company'])
            company = (await session.execute(stmt)).scalars().first()

            if not company:
                raise HTTPException(404)

            q = model(
                id=int(fact['id']),
                company_id=company.id,
                company=company,
                data1_fact=fact['data1'],
                data2_fact=fact['data2'],
                data1_forecast=forecast['data1'],
                data2_forecast=forecast['data2'],
                metric_date=self.generate_date(day)
            )
            logger.info(q)
            session.add(q)

            day += 1



