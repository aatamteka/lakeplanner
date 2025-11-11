"""Initial schema

Revision ID: 001_initial_schema
Revises:
Create Date: 2025-11-10 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('lakes',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('latitude', sa.Numeric(precision=10, scale=8), nullable=False),
    sa.Column('longitude', sa.Numeric(precision=11, scale=8), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_lakes_name'), 'lakes', ['name'], unique=False)

    op.create_table('users',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('preferred_lake_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('owns_boat', sa.Boolean(), nullable=True),
    sa.Column('preferred_marina_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('schedule_preferences', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('weather_preferences', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('notification_preferences', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)

    op.create_table('amenities',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('lake_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('type', sa.String(length=50), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('latitude', sa.Numeric(precision=10, scale=8), nullable=False),
    sa.Column('longitude', sa.Numeric(precision=11, scale=8), nullable=False),
    sa.Column('capacity_score', sa.Integer(), nullable=True),
    sa.Column('hours_of_operation', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('seasonal_availability', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.ForeignKeyConstraint(['lake_id'], ['lakes.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_amenities_lake_id'), 'amenities', ['lake_id'], unique=False)
    op.create_index(op.f('ix_amenities_type'), 'amenities', ['type'], unique=False)

    op.create_table('audit_log',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('event_type', sa.String(length=100), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('entity_type', sa.String(length=100), nullable=True),
    sa.Column('entity_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('payload', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_audit_log_created_at'), 'audit_log', ['created_at'], unique=False)
    op.create_index(op.f('ix_audit_log_event_type'), 'audit_log', ['event_type'], unique=False)
    op.create_index(op.f('ix_audit_log_user_id'), 'audit_log', ['user_id'], unique=False)

    op.create_table('boat_ramps',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('lake_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('latitude', sa.Numeric(precision=10, scale=8), nullable=False),
    sa.Column('longitude', sa.Numeric(precision=11, scale=8), nullable=False),
    sa.Column('hours_of_operation', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('seasonal_availability', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['lake_id'], ['lakes.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_boat_ramps_lake_id'), 'boat_ramps', ['lake_id'], unique=False)

    op.create_table('friendships',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('friend_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['friend_id'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'friend_id', name='uq_user_friend')
    )
    op.create_index(op.f('ix_friendships_friend_id'), 'friendships', ['friend_id'], unique=False)
    op.create_index(op.f('ix_friendships_status'), 'friendships', ['status'], unique=False)
    op.create_index(op.f('ix_friendships_user_id'), 'friendships', ['user_id'], unique=False)

    op.create_table('marinas',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('lake_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(255), nullable=False),
    sa.Column('latitude', sa.Numeric(precision=10, scale=8), nullable=False),
    sa.Column('longitude', sa.Numeric(precision=11, scale=8), nullable=False),
    sa.Column('rental_inventory', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('hours_of_operation', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['lake_id'], ['lakes.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_marinas_lake_id'), 'marinas', ['lake_id'], unique=False)

    op.create_table('outings',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('lake_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('planned_date', sa.Date(), nullable=False),
    sa.Column('time_slot', sa.String(length=20), nullable=False),
    sa.Column('target_amenities', postgresql.ARRAY(postgresql.UUID(as_uuid=True)), nullable=True),
    sa.Column('invited_friends', postgresql.ARRAY(postgresql.UUID(as_uuid=True)), nullable=True),
    sa.Column('rsvp_status', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['lake_id'], ['lakes.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_outings_lake_id'), 'outings', ['lake_id'], unique=False)
    op.create_index(op.f('ix_outings_planned_date'), 'outings', ['planned_date'], unique=False)
    op.create_index(op.f('ix_outings_time_slot'), 'outings', ['time_slot'], unique=False)
    op.create_index(op.f('ix_outings_user_id'), 'outings', ['user_id'], unique=False)

    op.create_table('weather_forecasts',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('lake_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('forecast_date', sa.Date(), nullable=False),
    sa.Column('temperature_high', sa.Numeric(precision=5, scale=2), nullable=True),
    sa.Column('temperature_low', sa.Numeric(precision=5, scale=2), nullable=True),
    sa.Column('precipitation_probability', sa.Integer(), nullable=True),
    sa.Column('wind_speed', sa.Numeric(precision=5, scale=2), nullable=True),
    sa.Column('conditions', sa.String(length=255), nullable=True),
    sa.Column('raw_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('fetched_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['lake_id'], ['lakes.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('lake_id', 'forecast_date', name='uq_lake_forecast_date')
    )
    op.create_index(op.f('ix_weather_forecasts_forecast_date'), 'weather_forecasts', ['forecast_date'], unique=False)
    op.create_index(op.f('ix_weather_forecasts_lake_id'), 'weather_forecasts', ['lake_id'], unique=False)

    op.create_table('amenity_contention',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('amenity_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('time_slot', sa.String(length=20), nullable=False),
    sa.Column('planned_groups_count', sa.Integer(), nullable=True),
    sa.Column('contention_score', sa.Numeric(precision=5, scale=2), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['amenity_id'], ['amenities.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('amenity_id', 'date', 'time_slot', name='uq_amenity_date_time')
    )
    op.create_index(op.f('ix_amenity_contention_amenity_id'), 'amenity_contention', ['amenity_id'], unique=False)
    op.create_index(op.f('ix_amenity_contention_contention_score'), 'amenity_contention', ['contention_score'], unique=False)
    op.create_index(op.f('ix_amenity_contention_date'), 'amenity_contention', ['date'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_amenity_contention_date'), table_name='amenity_contention')
    op.drop_index(op.f('ix_amenity_contention_contention_score'), table_name='amenity_contention')
    op.drop_index(op.f('ix_amenity_contention_amenity_id'), table_name='amenity_contention')
    op.drop_table('amenity_contention')
    op.drop_index(op.f('ix_weather_forecasts_lake_id'), table_name='weather_forecasts')
    op.drop_index(op.f('ix_weather_forecasts_forecast_date'), table_name='weather_forecasts')
    op.drop_table('weather_forecasts')
    op.drop_index(op.f('ix_outings_user_id'), table_name='outings')
    op.drop_index(op.f('ix_outings_time_slot'), table_name='outings')
    op.drop_index(op.f('ix_outings_planned_date'), table_name='outings')
    op.drop_index(op.f('ix_outings_lake_id'), table_name='outings')
    op.drop_table('outings')
    op.drop_index(op.f('ix_marinas_lake_id'), table_name='marinas')
    op.drop_table('marinas')
    op.drop_index(op.f('ix_friendships_user_id'), table_name='friendships')
    op.drop_index(op.f('ix_friendships_status'), table_name='friendships')
    op.drop_index(op.f('ix_friendships_friend_id'), table_name='friendships')
    op.drop_table('friendships')
    op.drop_index(op.f('ix_boat_ramps_lake_id'), table_name='boat_ramps')
    op.drop_table('boat_ramps')
    op.drop_index(op.f('ix_audit_log_user_id'), table_name='audit_log')
    op.drop_index(op.f('ix_audit_log_event_type'), table_name='audit_log')
    op.drop_index(op.f('ix_audit_log_created_at'), table_name='audit_log')
    op.drop_table('audit_log')
    op.drop_index(op.f('ix_amenities_type'), table_name='amenities')
    op.drop_index(op.f('ix_amenities_lake_id'), table_name='amenities')
    op.drop_table('amenities')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_lakes_name'), table_name='lakes')
    op.drop_table('lakes')
