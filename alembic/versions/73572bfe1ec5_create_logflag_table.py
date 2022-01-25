"""create logflag table

Revision ID: 73572bfe1ec5
Revises: 12b80cf462f6
Create Date: 2022-01-25 15:19:01.565927

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73572bfe1ec5'
down_revision = '12b80cf462f6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('logflag',
                    sa.Column('id', sa.Integer(),
                              nullable=False, primary_key=True),
                    sa.Column('name', sa.String(), nullable=False,),

                    )


def downgrade():
    op.drop_table('logflag')
