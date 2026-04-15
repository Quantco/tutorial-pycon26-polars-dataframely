from .data import RawData
from .preprocess import preprocess
from .report import Report, build_report


def run_pipeline(raw: RawData) -> Report:
    prep = preprocess(raw)
    report = build_report(prep)
    return report
