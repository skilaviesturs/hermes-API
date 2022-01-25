"""add all missing stuf

Revision ID: c708fcee3776
Revises: bb9283a26d79
Create Date: 2022-01-25 16:37:11.774400

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c708fcee3776'
down_revision = 'bb9283a26d79'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('computer', 'dnsname',
                    existing_type=sa.VARCHAR(),
                    nullable=True)
    op.alter_column('computer', 'created_at',
                    existing_type=postgresql.TIMESTAMP(timezone=True),
                    nullable=True,
                    existing_server_default=sa.text('now()'))
    op.alter_column('computer', 'owner_id',
                    existing_type=sa.INTEGER(),
                    nullable=True,
                    existing_server_default=sa.text('0'))
    op.create_index(op.f('ix_computer_id'), 'computer', ['id'], unique=False)
    op.add_column('disk', sa.Column(
        'id_computer', sa.Integer(), nullable=False))
    op.alter_column('disk', 'created_at',
                    existing_type=postgresql.TIMESTAMP(timezone=True),
                    nullable=True,
                    existing_server_default=sa.text('now()'))
    op.create_foreign_key(None, 'disk', 'computer', ['id_computer'], ['id'])
    op.add_column('events', sa.Column(
        'id_computer', sa.Integer(), nullable=False))
    op.alter_column('events', 'created_at',
                    existing_type=postgresql.TIMESTAMP(timezone=True),
                    nullable=True,
                    existing_server_default=sa.text('now()'))
    op.drop_constraint('events_event_time_key', 'events', type_='unique')
    op.drop_constraint('events_message_key', 'events', type_='unique')
    op.create_foreign_key(None, 'events', 'computer', ['id_computer'], ['id'])
    op.add_column('log', sa.Column('id_logflag', sa.Integer(),
                  server_default=sa.text('0'), nullable=True))
    op.add_column('log', sa.Column(
        'id_computer', sa.Integer(), nullable=False))
    op.alter_column('log', 'created_at',
                    existing_type=postgresql.TIMESTAMP(timezone=True),
                    nullable=True,
                    existing_server_default=sa.text('now()'))
    op.create_foreign_key(None, 'log', 'computer', ['id_computer'], ['id'])
    op.create_foreign_key(None, 'log', 'logflag', ['id_logflag'], ['id'])
    op.alter_column('owner', 'lastname',
                    existing_type=sa.VARCHAR(),
                    nullable=True)
    op.alter_column('owner', 'department',
                    existing_type=sa.VARCHAR(),
                    nullable=True)
    op.alter_column('owner', 'created_at',
                    existing_type=postgresql.TIMESTAMP(timezone=True),
                    nullable=True,
                    existing_server_default=sa.text('now()'))
    op.add_column('software', sa.Column(
        'id_computer', sa.Integer(), nullable=False))
    op.alter_column('software', 'created_at',
                    existing_type=postgresql.TIMESTAMP(timezone=True),
                    nullable=True,
                    existing_server_default=sa.text('now()'))
    op.drop_constraint('software_ident_number_key', 'software', type_='unique')
    op.drop_constraint('software_name_key', 'software', type_='unique')
    op.create_foreign_key(None, 'software', 'computer',
                          ['id_computer'], ['id'])
    op.add_column('users', sa.Column('password', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'password')
    op.drop_constraint(None, 'software', type_='foreignkey')
    op.create_unique_constraint('software_name_key', 'software', ['name'])
    op.create_unique_constraint(
        'software_ident_number_key', 'software', ['ident_number'])
    op.alter_column('software', 'created_at',
                    existing_type=postgresql.TIMESTAMP(timezone=True),
                    nullable=False,
                    existing_server_default=sa.text('now()'))
    op.drop_column('software', 'id_computer')
    op.alter_column('owner', 'created_at',
                    existing_type=postgresql.TIMESTAMP(timezone=True),
                    nullable=False,
                    existing_server_default=sa.text('now()'))
    op.alter_column('owner', 'department',
                    existing_type=sa.VARCHAR(),
                    nullable=False)
    op.alter_column('owner', 'lastname',
                    existing_type=sa.VARCHAR(),
                    nullable=False)
    op.drop_constraint(None, 'log', type_='foreignkey')
    op.drop_constraint(None, 'log', type_='foreignkey')
    op.alter_column('log', 'created_at',
                    existing_type=postgresql.TIMESTAMP(timezone=True),
                    nullable=False,
                    existing_server_default=sa.text('now()'))
    op.drop_column('log', 'id_computer')
    op.drop_column('log', 'id_logflag')
    op.drop_constraint(None, 'events', type_='foreignkey')
    op.create_unique_constraint('events_message_key', 'events', ['message'])
    op.create_unique_constraint(
        'events_event_time_key', 'events', ['event_time'])
    op.alter_column('events', 'created_at',
                    existing_type=postgresql.TIMESTAMP(timezone=True),
                    nullable=False,
                    existing_server_default=sa.text('now()'))
    op.drop_column('events', 'id_computer')
    op.drop_constraint(None, 'disk', type_='foreignkey')
    op.alter_column('disk', 'created_at',
                    existing_type=postgresql.TIMESTAMP(timezone=True),
                    nullable=False,
                    existing_server_default=sa.text('now()'))
    op.drop_column('disk', 'id_computer')
    op.drop_index(op.f('ix_computer_id'), table_name='computer')
    op.alter_column('computer', 'owner_id',
                    existing_type=sa.INTEGER(),
                    nullable=False,
                    existing_server_default=sa.text('0'))
    op.alter_column('computer', 'created_at',
                    existing_type=postgresql.TIMESTAMP(timezone=True),
                    nullable=False,
                    existing_server_default=sa.text('now()'))
    op.alter_column('computer', 'dnsname',
                    existing_type=sa.VARCHAR(),
                    nullable=False)
    # ### end Alembic commands ###
