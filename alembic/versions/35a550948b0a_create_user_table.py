"""create user table

Revision ID: 35a550948b0a
Revises: 
Create Date: 2022-01-25 00:57:09.691562

"""
from enum import unique
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35a550948b0a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(),
                              nullable=False, primary_key=True),
                    sa.Column('email', sa.String(),
                              nullable=False, unique=True),
                    sa.Column('disabled', sa.Boolean(),
                              server_default=sa.text('False')),
                    sa.Column('created_at', sa.String(), nullable=True),
                    sa.Column('updated_at', sa.String(), nullable=True),
                    )


def downgrade():
    op.drop_table('users')