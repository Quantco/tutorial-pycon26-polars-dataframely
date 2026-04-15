import polars as pl
import dataframely as dy

from ._internal import Report
from .data import PreprocessedData
from .schema.preprocessed import PrepModelsSchema, PrepPoliciesSchema
from .schema.report import (
    AverageCarVolumeSchema,
    PopularModelsSchema,
    SafestModelsSchema,
)


def build_report(prep: PreprocessedData) -> Report:
    return Report(
        popularity=find_three_most_popular_make_and_models(prep.models, prep.policies),
        safety=find_safest_models(prep.models),
        volume=find_average_car_volume_by_age(prep.models, prep.policies),
    )


def find_three_most_popular_make_and_models(
    models: dy.LazyFrame[PrepModelsSchema], policies: dy.LazyFrame[PrepPoliciesSchema]
) -> dy.LazyFrame[PopularModelsSchema]:
    """Among all policies, compute the three make/model combinations that appears most often.

    Returns:
        A dataframe with three rows and three columns (make, model, count).
    """
    return (
        policies.join(models, on="model")
        .group_by("make", "model")
        .agg(count=pl.len())
        .sort("count", descending=True)
        .head(3)
        .pipe(PopularModelsSchema.validate, cast=True, eager=False)
    )


def find_safest_models(
    models: dy.LazyFrame[PrepModelsSchema],
) -> dy.LazyFrame[SafestModelsSchema]:
    """Among all models, find the safest ones as measured by the number of safety features.

    Returns:
        A data frame with five rows and three columns (model, segment, safety_score).
    """
    return (
        models.select(
            "model", "segment", safety_score=pl.sum_horizontal(pl.col(pl.Boolean))
        )
        .sort("safety_score", descending=True)
        .head(5)
        .pipe(SafestModelsSchema.validate, cast=True, eager=False)
    )


def find_average_car_volume_by_age(
    models: dy.LazyFrame[PrepModelsSchema], policies: dy.LazyFrame[PrepPoliciesSchema]
) -> dy.LazyFrame[AverageCarVolumeSchema]:
    """Among all policies, find the mean physical car volume in 10-year blocks of car age.

    This method should compute the volume of a car if interpreted as cuboid (i.e. box-shaped).
    Blocks should be 0-10 years, 10-20 years, etc.

    Returns:
        A data frame with three columns (age block, mean volume in cubic meters,
        relative change of mean volume relative to the previous age block in percent).
    """
    volume = pl.col("length").cast(pl.UInt64) * pl.col("width") * pl.col("height")
    return (
        policies.join(models, on="model")
        .group_by(pl.col("age_of_car").cut(range(10, 100, 10)))
        .agg(volume=volume.mean() * 1e-9)
        .with_columns(
            change=100
            * (
                pl.col("volume") / pl.col("volume").shift().over(order_by="age_of_car")
                - 1
            )
        )
        .sort("age_of_car")
        .pipe(AverageCarVolumeSchema.validate, cast=True, eager=False)
    )
