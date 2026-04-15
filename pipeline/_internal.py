from dataclasses import dataclass

import polars as pl


@dataclass
class Report:
    popularity: pl.DataFrame | pl.LazyFrame
    safety: pl.DataFrame | pl.LazyFrame
    volume: pl.DataFrame | pl.LazyFrame

    def to_string(self) -> str:
        """
        Create a pretty-printable representation of this report.
        """
        # Enforce laziness and collection here to ensure we are
        #
        df_popularity, df_volume, df_safety = pl.collect_all(
            [
                self.popularity.lazy(),
                self.volume.lazy().sort("age_of_car"),
                self.safety.lazy(),
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
