from datetime import datetime
from typing import List, Any

from pydantic import BaseModel


class CompanyCreate(BaseModel):
    title: str


class CompanyUpdate(CompanyCreate):
    pass


class Company(CompanyCreate):
    id: int

    class Config:
        orm_mode = True


class MetricSchema(BaseModel):
    id: int
    company_id: int
    data1_fact: int
    data2_fact: int
    data1_forecast: int
    data2_forecast: int
    metric_date: Any

    class Config:
        orm_mode = True


class CompanyTotal(BaseModel):
    id: int
    title: str
    qliqs: List[MetricSchema]
    qoils: List[MetricSchema]

    class Config:
        orm_mode = True
