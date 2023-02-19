__all__ = ["aircraft_data", "airports", "boarding_passes", "bookings",
           "flights", "seats", "ticket_flights", "tickets"]


def to_dict(model_instance):
    return {c.name: getattr(model_instance, c.name) for c in model_instance.__table__.columns}
