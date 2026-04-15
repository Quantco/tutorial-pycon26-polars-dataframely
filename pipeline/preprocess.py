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
        # Categorical columns
        pl.col("model").cast(pl.Categorical),
        pl.col("area_cluster").cast(pl.Categorical),
        # Float columns often do not need full 64-bit precision
        # This depends on the domain we are working on
        pl.col("policy_tenure").cast(pl.Float32),
        pl.col("age_of_car").cast(pl.Float32),
        pl.col("age_of_policyholder").cast(pl.Float32),
        pl.col("population_density").cast(pl.Float32),
        # Normalize ID
        pl.col("policy_id").str.strip_prefix("policy").cast(pl.UInt64),
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
        max_torque_nm=torque_parts.list[0].str.strip_suffix("Nm").cast(pl.Float32),
        max_torque_rpm=torque_parts.list[1].str.strip_suffix("rpm").cast(pl.UInt16),
    )

    power_parts = pl.col("max_power").str.split("@")
    df = df.with_columns(
        max_power_bhp=power_parts.list[0].str.strip_suffix("bhp").cast(pl.Float16),
        max_power_rpm=power_parts.list[1].str.strip_suffix("rpm").cast(pl.UInt16),
    )

    # Step 3: Use efficient data types
    df = df.with_columns(
        # Some of the categorical columns are easily enumerated
        pl.col("steering_type").cast(pl.Enum(["Electric", "Manual", "Power"])),
        pl.col("fuel_type").cast(pl.Enum(["CNG", "Diesel", "Petrol"])),
        pl.col("rear_brakes_type").cast(pl.Enum(["Drum", "Disc"])),
        # For other categoricals, we may not be sure yet that we have seen all values
        # so we do not want to commit to an Enum, yet
        pl.col("engine_type").cast(pl.Categorical),
        pl.col("model").cast(pl.Categorical),
        pl.col("segment").cast(pl.Categorical),
        # Value-based dtypes
        pl.col("width").cast(pl.UInt16),
        pl.col("height").cast(pl.UInt16),
        pl.col("length").cast(pl.UInt16),
        pl.col("displacement").cast(pl.UInt16),
        pl.col("cylinder").cast(pl.UInt8),
        pl.col("gross_weight").cast(pl.UInt16),
        pl.col("gear_box").cast(pl.UInt8),
        pl.col("airbags").cast(pl.UInt8),
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
