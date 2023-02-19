# coding: utf-8
# coding: utf-8
from sqlalchemy import ARRAY, CHAR, CheckConstraint, Column, DateTime, ForeignKey, ForeignKeyConstraint, Integer, \
    Numeric, String, Table, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import INTERVAL, JSONB
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

t_aircrafts = Table(
    'aircrafts', metadata,
    Column('aircraft_code', CHAR(3), comment='Aircraft code, IATA'),
    Column('model', Text, comment='Aircraft model'),
    Column('range', Integer, comment='Maximal flying distance, km'),
    schema='bookings',
    comment='Aircrafts'
)


class AircraftsDatum(Base):
    __tablename__ = 'aircrafts_data'
    __table_args__ = (
        CheckConstraint('range > 0'),
        {'schema': 'bookings', 'comment': 'Aircrafts (internal data)'}
    )

    aircraft_code = Column(CHAR(3), primary_key=True, comment='Aircraft code, IATA')
    model = Column(JSONB(astext_type=Text()), nullable=False, comment='Aircraft model')
    range = Column(Integer, nullable=False, comment='Maximal flying distance, km')


t_airports = Table(
    'airports', metadata,
    Column('airport_code', CHAR(3), comment='Airport code'),
    Column('airport_name', Text, comment='Airport name'),
    Column('city', Text, comment='City'),
    Column('coordinates', NullType, comment='Airport coordinates (longitude and latitude)'),
    Column('timezone', Text, comment='Airport time zone'),
    schema='bookings',
    comment='Airports'
)


class AirportsDatum(Base):
    __tablename__ = 'airports_data'
    __table_args__ = {'schema': 'bookings', 'comment': 'Airports (internal data)'}

    airport_code = Column(CHAR(3), primary_key=True, comment='Airport code')
    airport_name = Column(JSONB(astext_type=Text()), nullable=False, comment='Airport name')
    city = Column(JSONB(astext_type=Text()), nullable=False, comment='City')
    coordinates = Column(NullType, nullable=False, comment='Airport coordinates (longitude and latitude)')
    timezone = Column(Text, nullable=False, comment='Airport time zone')


class Booking(Base):
    __tablename__ = 'bookings'
    __table_args__ = {'schema': 'bookings', 'comment': 'Bookings'}

    book_ref = Column(CHAR(6), primary_key=True, comment='Booking number')
    book_date = Column(DateTime(True), nullable=False, comment='Booking date')
    total_amount = Column(Numeric(10, 2), nullable=False, comment='Total booking cost')


t_flights_v = Table(
    'flights_v', metadata,
    Column('flight_id', Integer, comment='Flight ID'),
    Column('flight_no', CHAR(6), comment='Flight number'),
    Column('scheduled_departure', DateTime(True), comment='Scheduled departure time'),
    Column('scheduled_departure_local', DateTime,
           comment='Scheduled departure time, local time at the point of departure'),
    Column('scheduled_arrival', DateTime(True), comment='Scheduled arrival time'),
    Column('scheduled_arrival_local', DateTime,
           comment='Scheduled arrival time, local time at the point of destination'),
    Column('scheduled_duration', INTERVAL, comment='Scheduled flight duration'),
    Column('departure_airport', CHAR(3), comment='Deprature airport code'),
    Column('departure_airport_name', Text, comment='Departure airport name'),
    Column('departure_city', Text, comment='City of departure'),
    Column('arrival_airport', CHAR(3), comment='Arrival airport code'),
    Column('arrival_airport_name', Text, comment='Arrival airport name'),
    Column('arrival_city', Text, comment='City of arrival'),
    Column('status', String(20), comment='Flight status'),
    Column('aircraft_code', CHAR(3), comment='Aircraft code, IATA'),
    Column('actual_departure', DateTime(True), comment='Actual departure time'),
    Column('actual_departure_local', DateTime, comment='Actual departure time, local time at the point of departure'),
    Column('actual_arrival', DateTime(True), comment='Actual arrival time'),
    Column('actual_arrival_local', DateTime, comment='Actual arrival time, local time at the point of destination'),
    Column('actual_duration', INTERVAL, comment='Actual flight duration'),
    schema='bookings',
    comment='Flights (extended)'
)

t_routes = Table(
    'routes', metadata,
    Column('flight_no', CHAR(6), comment='Flight number'),
    Column('departure_airport', CHAR(3), comment='Code of airport of departure'),
    Column('departure_airport_name', Text, comment='Name of airport of departure'),
    Column('departure_city', Text, comment='City of departure'),
    Column('arrival_airport', CHAR(3), comment='Code of airport of arrival'),
    Column('arrival_airport_name', Text, comment='Name of airport of arrival'),
    Column('arrival_city', Text, comment='City of arrival'),
    Column('aircraft_code', CHAR(3), comment='Aircraft code, IATA'),
    Column('duration', INTERVAL, comment='Scheduled duration of flight'),
    Column('days_of_week', ARRAY(Integer()), comment='Days of week on which flights are scheduled'),
    schema='bookings',
    comment='Routes'
)


class Flight(Base):
    __tablename__ = 'flights'
    __table_args__ = (
        CheckConstraint(
            '(actual_arrival IS NULL) OR ((actual_departure IS NOT NULL) AND (actual_arrival IS NOT NULL) AND (actual_arrival > actual_departure))'),
        CheckConstraint(
            "(status)::text = ANY (ARRAY[('On Time'::character varying)::text, ('Delayed'::character varying)::text, ('Departed'::character varying)::text, ('Arrived'::character varying)::text, ('Scheduled'::character varying)::text, ('Cancelled'::character varying)::text])"),
        CheckConstraint('scheduled_arrival > scheduled_departure'),
        UniqueConstraint('flight_no', 'scheduled_departure'),
        {'schema': 'bookings', 'comment': 'Flights'}
    )

    flight_id = Column(Integer, primary_key=True,
                       server_default=text("nextval('\"bookings\".flights_flight_id_seq'::regclass)"),
                       comment='Flight ID')
    flight_no = Column(CHAR(6), nullable=False, comment='Flight number')
    scheduled_departure = Column(DateTime(True), nullable=False, comment='Scheduled departure time')
    scheduled_arrival = Column(DateTime(True), nullable=False, comment='Scheduled arrival time')
    departure_airport = Column(ForeignKey('bookings.airports_data.airport_code'), nullable=False,
                               comment='Airport of departure')
    arrival_airport = Column(ForeignKey('bookings.airports_data.airport_code'), nullable=False,
                             comment='Airport of arrival')
    status = Column(String(20), nullable=False, comment='Flight status')
    aircraft_code = Column(ForeignKey('bookings.aircrafts_data.aircraft_code'), nullable=False,
                           comment='Aircraft code, IATA')
    actual_departure = Column(DateTime(True), comment='Actual departure time')
    actual_arrival = Column(DateTime(True), comment='Actual arrival time')

    aircrafts_datum = relationship('AircraftsDatum')
    airports_datum = relationship('AirportsDatum', primaryjoin='Flight.arrival_airport == AirportsDatum.airport_code')
    airports_datum1 = relationship('AirportsDatum',
                                   primaryjoin='Flight.departure_airport == AirportsDatum.airport_code')


class Seat(Base):
    __tablename__ = 'seats'
    __table_args__ = (
        CheckConstraint(
            "(fare_conditions)::text = ANY (ARRAY[('Economy'::character varying)::text, ('Comfort'::character varying)::text, ('Business'::character varying)::text])"),
        {'schema': 'bookings', 'comment': 'Seats'}
    )

    aircraft_code = Column(ForeignKey('bookings.aircrafts_data.aircraft_code', ondelete='CASCADE'), primary_key=True,
                           nullable=False, comment='Aircraft code, IATA')
    seat_no = Column(String(4), primary_key=True, nullable=False, comment='Seat number')
    fare_conditions = Column(String(10), nullable=False, comment='Travel class')

    aircrafts_datum = relationship('AircraftsDatum')


class Ticket(Base):
    __tablename__ = 'tickets'
    __table_args__ = {'schema': 'bookings', 'comment': 'Tickets'}

    ticket_no = Column(CHAR(13), primary_key=True, comment='Ticket number')
    book_ref = Column(ForeignKey('bookings.bookings.book_ref'), nullable=False, comment='Booking number')
    passenger_id = Column(String(20), nullable=False, comment='Passenger ID')
    passenger_name = Column(Text, nullable=False, comment='Passenger name')
    contact_data = Column(JSONB(astext_type=Text()), comment='Passenger contact information')

    booking = relationship('Booking')


class TicketFlight(Base):
    __tablename__ = 'ticket_flights'
    __table_args__ = (
        CheckConstraint(
            "(fare_conditions)::text = ANY (ARRAY[('Economy'::character varying)::text, ('Comfort'::character varying)::text, ('Business'::character varying)::text])"),
        CheckConstraint('amount >= (0)::numeric'),
        {'schema': 'bookings', 'comment': 'Flight segment'}
    )

    ticket_no = Column(ForeignKey('bookings.tickets.ticket_no'), primary_key=True, nullable=False,
                       comment='Ticket number')
    flight_id = Column(ForeignKey('bookings.flights.flight_id'), primary_key=True, nullable=False, comment='Flight ID')
    fare_conditions = Column(String(10), nullable=False, comment='Travel class')
    amount = Column(Numeric(10, 2), nullable=False, comment='Travel cost')

    flight = relationship('Flight')
    ticket = relationship('Ticket')


class BoardingPass(TicketFlight):
    __tablename__ = 'boarding_passes'
    __table_args__ = (
        ForeignKeyConstraint(['ticket_no', 'flight_id'],
                             ['bookings.ticket_flights.ticket_no', 'bookings.ticket_flights.flight_id']),
        UniqueConstraint('flight_id', 'boarding_no'),
        UniqueConstraint('flight_id', 'seat_no'),
        {'schema': 'bookings', 'comment': 'Boarding passes'}
    )

    ticket_no = Column(CHAR(13), primary_key=True, nullable=False, comment='Ticket number')
    flight_id = Column(Integer, primary_key=True, nullable=False, comment='Flight ID')
    boarding_no = Column(Integer, nullable=False, comment='Boarding pass number')
    seat_no = Column(String(4), nullable=False, comment='Seat number')
