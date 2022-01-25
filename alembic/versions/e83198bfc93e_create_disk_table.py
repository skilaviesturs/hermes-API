"""create disk table

Revision ID: e83198bfc93e
Revises: 0b3f55a3cf5a
Create Date: 2022-01-25 15:05:24.458004

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e83198bfc93e'
down_revision = '0b3f55a3cf5a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('disk',
                    sa.Column('id', sa.Integer(),
                              nullable=False, primary_key=True),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('size', sa.String(), nullable=False),
                    sa.Column('free', sa.String(), nullable=False),
                    sa.Column('disk_type', sa.String(), nullable=True),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(
                              timezone=True), nullable=True),
                    )


def downgrade():
    op.drop_table('disk')
