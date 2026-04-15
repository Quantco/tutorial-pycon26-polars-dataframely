from dataclasses import dataclass
import dataframely as dy

from .schema.preprocessed import PrepPoliciesSchema, PrepModelsSchema
from .schema.raw import RawModelsSchema, RawPoliciesSchema


@dataclass
class RawData:
    models: dy.LazyFrame[RawModelsSchema]
    policies: dy.LazyFrame[RawPoliciesSchema]


@dataclass
class PreprocessedData:
    models: dy.LazyFrame[PrepModelsSchema]
    policies: dy.LazyFrame[PrepPoliciesSchema]
