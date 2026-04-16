import dataframely as dy
import polars as pl


class PrepPoliciesSchema(dy.Schema):
    policy_id = dy.UInt64(primary_key=True)
    policy_tenure = dy.Float32()
    age_of_car = dy.Float32()
    age_of_policyholder = dy.Float32()
    area_cluster = dy.Categorical()
    population_density = dy.Float32()
    model = dy.Categorical(nullable=True)


class PrepModelsSchema(dy.Schema):
    model = dy.Categorical(primary_key=True)
    segment = dy.Categorical()
    fuel_type = dy.Enum(["CNG", "Diesel", "Petrol"])
    airbags = dy.UInt8()
    is_esc = dy.Bool()
    is_adjustable_steering = dy.Bool()
    is_tpms = dy.Bool()
    is_parking_sensors = dy.Bool()
    is_parking_camera = dy.Bool()
    rear_brakes_type = dy.Enum(["Drum", "Disc"])
    displacement = dy.UInt16()
    cylinder = dy.UInt8()
    transmission_type = dy.String()
    gear_box = dy.UInt8()
    steering_type = dy.Enum(["Electric", "Manual", "Power"])
    turning_radius = dy.Float64()
    length = dy.UInt16()
    width = dy.UInt16()
    height = dy.UInt16()
    gross_weight = dy.UInt16()
    is_front_fog_lights = dy.Bool()
    is_rear_window_wiper = dy.Bool()
    is_rear_window_washer = dy.Bool()
    is_rear_window_defogger = dy.Bool()
    is_brake_assist = dy.Bool()
    is_power_door_locks = dy.Bool()
    is_central_locking = dy.Bool()
    is_power_steering = dy.Bool()
    is_driver_seat_height_adjustable = dy.Bool()
    is_day_night_rear_view_mirror = dy.Bool()
    is_ecw = dy.Bool()
    is_speed_alert = dy.Bool()
    ncap_rating = dy.Int64()
    engine_type = dy.Categorical()
    make = dy.Int64()
    max_torque_nm = dy.Float32()
    max_torque_rpm = dy.UInt16()
    max_power_bhp = dy.Float32()
    max_power_rpm = dy.UInt16()

    @dy.rule()
    def volume_is_realistic(cls) -> pl.Expr:
        """Only allow reasonably sized cars"""
        volume = cls.length.col.cast(pl.UInt64) * cls.width.col * cls.height.col

        # Lengths are in millimeters and 1e9 mm^3 is 1 cubic meter
        cubic_meter = 1e9
        return volume.is_between(1 * cubic_meter, 20 * cubic_meter)
