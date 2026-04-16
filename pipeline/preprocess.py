import polars as pl
import dataframely as dy
from .data import PreprocessedData, RawData
from .schema.preprocessed import PrepModelsSchema, PrepPoliciesSchema
from .schema.raw import RawModelsSchema, RawPoliciesSchema


def preprocess(raw: RawData) -> PreprocessedData:
    return PreprocessedData(
        policies=raw.policies.pipe(preprocess_policies),
        models=raw.models.pipe(preprocess_models),
    )


def preprocess_policies(
    policies: dy.LazyFrame[RawPoliciesSchema],
) -> dy.LazyFrame[PrepPoliciesSchema]:
    """Transform the raw policies for optimal representation."""
    return policies.with_columns(
        # Normalize ID
        pl.col("policy_id").str.strip_prefix("policy"),
    ).pipe(PrepPoliciesSchema.validate, cast=True, eager=False)


def preprocess_models(
    models: dy.LazyFrame[RawModelsSchema],
) -> dy.LazyFrame[PrepModelsSchema]:
    """Transform the raw models for optimal representation."""

    # Unique to drop duplicate rows we found while investigating primary key failures
    df = models.unique()

    # 1. Convert semantically boolean columns from pl.String to pl.Boolean
    df = df.with_columns(pl.col("^is_.*$") == "Yes")

    # 2. Split max torque and power into components
    torque_parts = pl.col("max_torque").str.split("@")
    df = df.with_columns(
        max_torque_nm=torque_parts.list[0].str.strip_suffix("Nm"),
        max_torque_rpm=torque_parts.list[1].str.strip_suffix("rpm"),
    )

    power_parts = pl.col("max_power").str.split("@")
    df = df.with_columns(
        max_power_bhp=power_parts.list[0].str.strip_suffix("bhp"),
        max_power_rpm=power_parts.list[1].str.strip_suffix("rpm"),
    )

    # Step 4: Ensure that length / width / height are in millimeters, not centimeters
    def _ensure_mm(col: pl.Expr):
        return pl.when(col < 1_000).then(col * 10).otherwise(col)

    df = df.with_columns(
        _ensure_mm(pl.col("length")),
        _ensure_mm(pl.col("width")),
        _ensure_mm(pl.col("height")),
    )

    return df.pipe(PrepModelsSchema.validate, cast=True, eager=False)
