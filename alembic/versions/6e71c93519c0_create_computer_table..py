"""create computer table

Revision ID: 6e71c93519c0
Revises: 35a550948b0a
Create Date: 2022-01-25 14:04:37.768904

"""
from enum import unique
from time import timezone
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e71c93519c0'
down_revision = '35a550948b0a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('computer',
                    sa.Column('id', sa.Integer(),
                              nullable=False, primary_key=True),
                    sa.Column('name', sa.String(),
                              nullable=False, unique=True),
                    sa.Column('dnsname', sa.String(),
                              nullable=False, unique=True),
                    sa.Column('location', sa.String(), nullable=True),
                    sa.Column('cpu', sa.String(), nullable=True),
                    sa.Column('ram', sa.String(), nullable=True),
                    sa.Column('ipv4', sa.String(), nullable=True, unique=True),
                    sa.Column('mac', sa.String(), nullable=True, unique=True),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(
                        timezone=True), nullable=True),
                    )


def downgrade():
    op.drop_table('computer')
