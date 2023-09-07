"""Userテーブルのtoken削除

Revision ID: 1ff922047346
Revises: e670c919ebae
Create Date: 2023-09-07 12:21:47.796385

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1ff922047346'
down_revision: Union[str, None] = 'e670c919ebae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('users', 'token')
    pass


def downgrade() -> None:
    op.add_column('tasks', sa.Column('token', sa.String(length=255), nullable=True))
    pass
