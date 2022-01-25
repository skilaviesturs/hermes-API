"""create software table

Revision ID: 547c6053dccd
Revises: f4c709a90e0c
Create Date: 2022-01-25 15:13:26.236326

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '547c6053dccd'
down_revision = 'f4c709a90e0c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('software',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('name', sa.String(), nullable=False, unique=True),
        sa.Column('ident_number', sa.String(), nullable=False, unique=True),
        sa.Column('version', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
            server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=True),
        )


def downgrade():
    op.drop_table('software')
