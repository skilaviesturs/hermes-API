"""create owner table

Revision ID: 0b3f55a3cf5a
Revises: 6e71c93519c0
Create Date: 2022-01-25 15:01:56.451747

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b3f55a3cf5a'
down_revision = '6e71c93519c0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('owner',
                    sa.Column('id', sa.Integer(),
                              nullable=False, primary_key=True),
                    sa.Column('firstname', sa.String(), nullable=False),
                    sa.Column('lastname', sa.String(), nullable=False),
                    sa.Column('department', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(
                        timezone=True), nullable=True),
                    )


def downgrade():
    op.drop_table('owner')
