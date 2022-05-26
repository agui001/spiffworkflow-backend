"""empty message

Revision ID: dec9751e0e3d
Revises: 
Create Date: 2022-05-26 16:18:46.472592

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dec9751e0e3d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin_session',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=50), nullable=True),
    sa.Column('admin_impersonate_uid', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token')
    )
    op.create_table('group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('new_name_two', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('uid', sa.String(length=50), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uid'),
    sa.UniqueConstraint('username')
    )
    op.create_table('process_instance',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('process_model_identifier', sa.String(), nullable=False),
    sa.Column('bpmn_json', sa.JSON(), nullable=True),
    sa.Column('start_in_seconds', sa.Integer(), nullable=True),
    sa.Column('end_in_seconds', sa.Integer(), nullable=True),
    sa.Column('process_initiator_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('not_started', 'user_input_required', 'waiting', 'complete', 'erroring', name='processinstancestatus'), nullable=True),
    sa.ForeignKeyConstraint(['process_initiator_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_process_instance_process_model_identifier'), 'process_instance', ['process_model_identifier'], unique=False)
    op.create_table('user_group_assignment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'group_id', name='user_group_assignment_unique')
    )
    op.create_table('file',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('content_type', sa.String(), nullable=False),
    sa.Column('process_instance_id', sa.Integer(), nullable=True),
    sa.Column('task_spec', sa.String(), nullable=True),
    sa.Column('irb_doc_code', sa.String(), nullable=False),
    sa.Column('md5_hash', sa.String(), nullable=False),
    sa.Column('data', sa.LargeBinary(), nullable=True),
    sa.Column('size', sa.Integer(), nullable=True),
    sa.Column('date_modified', sa.DateTime(timezone=True), nullable=True),
    sa.Column('date_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('user_uid', sa.String(), nullable=True),
    sa.Column('archived', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['process_instance_id'], ['process_instance.id'], ),
    sa.ForeignKeyConstraint(['user_uid'], ['user.uid'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('task_event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_uid', sa.String(), nullable=False),
    sa.Column('process_instance_id', sa.Integer(), nullable=False),
    sa.Column('spec_version', sa.String(), nullable=True),
    sa.Column('action', sa.String(), nullable=True),
    sa.Column('task_id', sa.String(), nullable=True),
    sa.Column('task_name', sa.String(), nullable=True),
    sa.Column('task_title', sa.String(), nullable=True),
    sa.Column('task_type', sa.String(), nullable=True),
    sa.Column('task_state', sa.String(), nullable=True),
    sa.Column('task_lane', sa.String(), nullable=True),
    sa.Column('form_data', sa.JSON(), nullable=True),
    sa.Column('mi_type', sa.String(), nullable=True),
    sa.Column('mi_count', sa.Integer(), nullable=True),
    sa.Column('mi_index', sa.Integer(), nullable=True),
    sa.Column('process_name', sa.String(), nullable=True),
    sa.Column('date', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['process_instance_id'], ['process_instance.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('data_store',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('last_updated', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('key', sa.String(), nullable=False),
    sa.Column('process_instance_id', sa.Integer(), nullable=True),
    sa.Column('task_spec', sa.String(), nullable=True),
    sa.Column('spec_id', sa.String(), nullable=True),
    sa.Column('user_id', sa.String(), nullable=True),
    sa.Column('file_id', sa.Integer(), nullable=True),
    sa.Column('value', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['file_id'], ['file.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('data_store')
    op.drop_table('task_event')
    op.drop_table('file')
    op.drop_table('user_group_assignment')
    op.drop_index(op.f('ix_process_instance_process_model_identifier'), table_name='process_instance')
    op.drop_table('process_instance')
    op.drop_table('user')
    op.drop_table('group')
    op.drop_table('admin_session')
    # ### end Alembic commands ###
