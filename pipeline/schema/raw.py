import dataframely as dy


class RawPoliciesSchema(dy.Schema):
    """Schema for the raw policies table as provided by our data source"""

    policy_id = dy.String(primary_key=True)
    policy_tenure = dy.Float64()
    age_of_car = dy.Float64()
    age_of_policyholder = dy.Float64()
    area_cluster = dy.String()
    population_density = dy.Int64()
    model = dy.String(nullable=True)


class RawModelsSchema(dy.Schema):
    """Schema for the raw models table as provided by our data source"""

    model = dy.String()
    segment = dy.String()
    fuel_type = dy.String()
    airbags = dy.Int64()
    is_esc = dy.String()
    is_adjustable_steering = dy.String()
    is_tpms = dy.String()
    is_parking_sensors = dy.String()
    is_parking_camera = dy.String()
    rear_brakes_type = dy.String()
    displacement = dy.Int64()
    cylinder = dy.Int64()
    transmission_type = dy.String()
    gear_box = dy.Int64()
    steering_type = dy.String()
    turning_radius = dy.Float64()
    length = dy.Float64()
    width = dy.Float64()
    height = dy.Float64()
    gross_weight = dy.Int64()
    is_front_fog_lights = dy.String()
    is_rear_window_wiper = dy.String()
    is_rear_window_washer = dy.String()
    is_rear_window_defogger = dy.String()
    is_brake_assist = dy.String()
    is_power_door_locks = dy.String()
    is_central_locking = dy.String()
    is_power_steering = dy.String()
    is_driver_seat_height_adjustable = dy.String()
    is_day_night_rear_view_mirror = dy.String()
    is_ecw = dy.String()
    is_speed_alert = dy.String()
    ncap_rating = dy.Int64()
    engine_type = dy.String()
    make = dy.UInt64()
    max_power = dy.String()
    max_torque = dy.String()
