"""add foregin keys to tables

Revision ID: bb9283a26d79
Revises: 73572bfe1ec5
Create Date: 2022-01-25 16:05:37.181735

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb9283a26d79'
down_revision = '73572bfe1ec5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('computer',
                  sa.Column('owner_id',
                            sa.Integer(), nullable=False,
                            server_default=sa.text('0'))
                  )
    op.create_foreign_key('computer_owner_fk',
                          source_table='computer',
                          referent_table='owner',
                          local_cols=['owner_id'],
                          remote_cols=['id']
                          )


def downgrade():
    op.drop_constraint('computer_owner_fk', table_name='computer')
    op.drop_column('computer','owner_id')
