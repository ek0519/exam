"""create user table

Revision ID: bd4e43ba2311
Revises: 
Create Date: 2022-04-29 10:25:29.799857

"""
import datetime

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'bd4e43ba2311'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('created_at', sa.TIMESTAMP(), default=datetime.datetime.utcnow),
        sa.Column('updated_at', sa.TIMESTAMP(), default=datetime.datetime.utcnow),
        sa.Column('last_login_at', sa.TIMESTAMP(), nullable=True),
        sa.Column('name', sa.String(255), unique=True, nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password', sa.String(255), nullable=False),
        sa.Column('remember_me', sa.String(255), nullable=False),
        sa.Column('is_verify', sa.Boolean(), default=False),
        sa.Column('verify_token', sa.String(255), nullable=True),
        sa.Column('is_verify', sa.Boolean(), default=False),
        sa.Column('last_login_ip', sa.String(15), nullable=True),
    )
    op.create_index('idx_users', 'users', ['name', 'email', 'verify_token'])


def downgrade():
    op.drop_table('users')
