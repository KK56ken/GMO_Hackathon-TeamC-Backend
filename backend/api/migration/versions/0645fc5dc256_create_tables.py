"""create tables

Revision ID: 0645fc5dc256
Revises: 
Create Date: 2023-09-06 02:54:47.607367

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0645fc5dc256'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('departments',
    sa.Column('department_id', sa.Integer(), nullable=False),
    sa.Column('department_name', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('department_id')
    )
    op.create_table('skills',
    sa.Column('skill_id', sa.Integer(), nullable=False),
    sa.Column('skill_name', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('skill_id')
    )
    op.create_table('tasks',
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('task_detail', sa.String(length=255), nullable=True),
    sa.Column('concern_desc', sa.String(length=255), nullable=True),
    sa.Column('ticket_link', sa.String(length=255), nullable=True),
    sa.Column('end_flag', sa.Integer(), nullable=True),
    sa.Column('register_date', sa.String(length=255), nullable=True),
    sa.Column('end_date', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('task_id')
    )
    op.create_table('tasks_skills',
    sa.Column('task_skill_id', sa.Integer(), nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=True),
    sa.Column('skill_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('task_skill_id')
    )
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('email',sa.String(length=255),nullable=True),
    sa.Column('password',sa.String(length=255),nullable=True),
    sa.Column('status',sa.Integer(),nullable=True),
    sa.Column('depart_id',sa.Integer(),nullable=True),
    sa.Column('slack_id',sa.String(length=255),nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('users_skills',
    sa.Column('user_skill_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('skill_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('user_skill_id')
    )
                    


    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
