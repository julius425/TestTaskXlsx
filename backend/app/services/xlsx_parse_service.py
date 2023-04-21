from io import BytesIO
import typing as t

import pandas as pd


class XlsxParseService:
    """Main mechanic is to split on fact\fore and next on qli qoil
    """

    def __init__(self, xlsx_bytz: bytes):
        self.df = pd.read_excel(BytesIO(xlsx_bytz), header=0)
        self._fact_column_name = 'fact'
        self._forecast_column_name = 'forecast'
        self._initial_column_mapping = {
            "Unnamed: 3":"fact",
            "Unnamed: 4":"fact",
            "Unnamed: 5":"fact",
            "Unnamed: 7":"forecast",
            "Unnamed: 8":"forecast",
            "Unnamed: 9":"forecast",
        }
        self.fact_qliq: t.List[t.Dict] | None = None
        self.fact_qoil: t.List[t.Dict] | None = None
        self.forecast_qliq: t.List[t.Dict] | None = None
        self.forecast_qoil: t.List[t.Dict] | None = None

    def _normalize_initial_columns(self):
        """renaming column names due to pandas xlsx merged
        columns import traits"""
        self.df = self.df.rename(columns=self._initial_column_mapping)
        # self.df['id'] = self.df['id'].astype(int)

    def _make_fact_forecast_dataframe(self, column_name) -> pd.DataFrame:
        """split initial df on fact and forecast data"""
        return self.df[['id', 'company', column_name]]

    def _make_qliq_qoil_dataframe(self, fact_df: pd.DataFrame):
        """qlick and qoil data combined df"""
        fact_df.columns = fact_df.iloc[0]
        # remove first row from the dataframe rows
        qliq_qoil_df = fact_df[1:]
        # rename rows (unmerged traits)
        qliq_qoil_df.columns = ['id', 'company', 'Qliq', 'Qliq', 'Qoil', 'Qoil']
        return qliq_qoil_df

    def _get_metrick_dataframe(self, qlik_qoil_df, column_name):
        """split combined df on Qlick or Qoil data"""
        metric_df = qlik_qoil_df[['id', 'company', column_name]]
        metric_df.columns = metric_df.iloc[0]
        metric_df = metric_df[1:]
        metric_df.columns = ['id', 'company', 'data1', 'data2']
        return metric_df.to_dict(orient='records')

    def parse(self):
        self._normalize_initial_columns()

        # process data
        fact = self._make_fact_forecast_dataframe('fact')
        forecast = self._make_fact_forecast_dataframe('forecast')

        fact_qliq_qoil = self._make_qliq_qoil_dataframe(fact)
        forecast_qliq_qoil = self._make_qliq_qoil_dataframe(forecast)

        # make dicts out of dataframes
        self.fact_qliq = self._get_metrick_dataframe(fact_qliq_qoil, 'Qliq')
        self.fact_qoil = self._get_metrick_dataframe(fact_qliq_qoil, 'Qoil')
        self.forecast_qliq = self._get_metrick_dataframe(forecast_qliq_qoil, 'Qliq')
        self.forecast_qoil = self._get_metrick_dataframe(forecast_qliq_qoil, 'Qoil')

