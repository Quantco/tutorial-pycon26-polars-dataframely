from pipeline.schema.preprocessed import PrepModelsSchema, PrepPoliciesSchema
from pipeline.schema.report import AverageCarVolumeSchema
from pipeline.report import find_average_car_volume_by_age
import polars as pl
from polars.testing import assert_frame_equal


def test_find_average_car_volume_by_age():
    # Arrange
    models = PrepModelsSchema.sample(
        overrides=[
            {"model": "M1", "height": 1_500, "width": 2_000, "length": 2_500},
            {"model": "M2", "height": 2_000, "width": 2_000, "length": 2_000},
        ]
    )
    policies = PrepPoliciesSchema.sample(
        overrides=[
            {"model": "M1", "age_of_car": 4.5},
            {"model": "M2", "age_of_car": 14.5},
        ]
    )

    volume_m1 = 1e-9 * 1_500 * 2_000 * 2_500
    volume_m2 = 1e-9 * 2_000 * 2_000 * 2_000
    change = 100 * (volume_m2 / volume_m1 - 1)
    expected = AverageCarVolumeSchema.validate(
        pl.DataFrame(
            [
                {"age_of_car": "(-inf, 10]", "volume": volume_m1, "change": None},
                {"age_of_car": "(10, 20]", "volume": volume_m2, "change": change},
            ]
        ),
        cast=True,
    ).lazy()

    # Act
    df = find_average_car_volume_by_age(models, policies)

    # Assert
    assert_frame_equal(expected, df)
