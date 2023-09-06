"""name変更

Revision ID: e670c919ebae
Revises: 0645fc5dc256
Create Date: 2023-09-06 07:06:51.686409

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'e670c919ebae'
down_revision: Union[str, None] = '0645fc5dc256'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('task_detail', sa.String(length=255), nullable=True))
    op.drop_column('tasks', 'tasks_detail')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('tasks_detail', mysql.VARCHAR(length=255), nullable=True))
    op.drop_column('tasks', 'task_detail')
    # ### end Alembic commands ###
