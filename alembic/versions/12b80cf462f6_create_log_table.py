"""create log table

Revision ID: 12b80cf462f6
Revises: 547c6053dccd
Create Date: 2022-01-25 15:15:50.340830

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12b80cf462f6'
down_revision = '547c6053dccd'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('log',
                    sa.Column('id', sa.Integer(),
                              nullable=False, primary_key=True),
                    sa.Column('message', sa.String(), nullable=False,),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),

                    )


def downgrade():
    op.drop_table('log')
