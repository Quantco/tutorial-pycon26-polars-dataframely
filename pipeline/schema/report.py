import dataframely as dy


class PopularModelsSchema(dy.Schema):
    make = dy.String()
    model = dy.String(primary_key=True)
    count = dy.UInt32()


class SafestModelsSchema(dy.Schema):
    model = dy.Categorical(primary_key=True)
    segment = dy.Categorical()
    safety_score = dy.UInt16()


class AverageCarVolumeSchema(dy.Schema):
    age_of_car = dy.String(primary_key=True)
    volume = dy.Float32()
    change = dy.Float32(nullable=True)
