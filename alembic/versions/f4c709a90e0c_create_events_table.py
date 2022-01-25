"""create events table

Revision ID: f4c709a90e0c
Revises: e83198bfc93e
Create Date: 2022-01-25 15:09:48.242753

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4c709a90e0c'
down_revision = 'e83198bfc93e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('events',
                    sa.Column('id', sa.Integer(),
                              nullable=False, primary_key=True),
                    sa.Column('event_time', sa.String(),
                              nullable=False, unique=True),
                    sa.Column('message', sa.String(),
                              nullable=False, unique=True),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    )


def downgrade():
    op.drop_table('events')
