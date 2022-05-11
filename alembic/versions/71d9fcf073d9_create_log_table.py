"""create log table

Revision ID: 71d9fcf073d9
Revises: bd4e43ba2311
Create Date: 2022-04-29 10:43:50.783265

"""
import datetime

import sqlalchemy as sa
from alembic import op
# revision identifiers, used by Alembic.
from sqlalchemy import ForeignKey

revision = '71d9fcf073d9'
down_revision = 'bd4e43ba2311'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'logs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('created_at', sa.TIMESTAMP(), default=datetime.datetime.utcnow),
        sa.Column('user_id', sa.Integer, ForeignKey('users.id'), nullable=False),
        sa.Column('ip', sa.String(255), nullable=True),
    )


def downgrade():
    op.drop_table('logs')
