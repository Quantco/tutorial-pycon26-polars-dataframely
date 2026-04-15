from dataclasses import dataclass
import polars as pl
import dataframely as dy
from .schema.report import (
    AverageCarVolumeSchema,
    PopularModelsSchema,
    SafestModelsSchema,
)


@dataclass
class Report:
    popularity: dy.LazyFrame[PopularModelsSchema]
    safety: dy.LazyFrame[SafestModelsSchema]
    volume: dy.LazyFrame[AverageCarVolumeSchema]

    def to_string(self) -> str:
        """
        Create a pretty-printable representation of this report.
        """
        df_popularity, df_volume, df_safety = pl.collect_all(
            [
                self.popularity,
                self.volume,
                self.safety,
            ]
        )
        header = [
            "",
            "=" * 60,
            "REPORT".center(60),
            "=" * 60,
            "",
        ]

        popularity = [
            "Top 3 Most Popular Make/Model Combinations:",
            "-" * 60,
            str(df_popularity),
        ]

        safety = [
            "Top 5 Safest Models:",
            "-" * 60,
            str(df_safety),
        ]

        volume = [
            "",
            "",
            "Average Car Volume by Age:",
            "-" * 60,
            str(df_volume),
        ]

        footer = [
            "",
            "=" * 60,
        ]

        return "\n".join(header + popularity + safety + volume + footer)
