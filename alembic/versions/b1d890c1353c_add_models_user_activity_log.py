"""add models user_activity_log

Revision ID: b1d890c1353c
Revises: 4fc340f6f399
Create Date: 2025-02-20 14:48:14.555484

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'b1d890c1353c'
down_revision: Union[str, None] = '4fc340f6f399'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'user_activity_log',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_uuid', sa.String(length=255), nullable=False),
        sa.Column('package_name', sa.String(length=255), nullable=False),
        sa.Column('content', sa.JSON(), nullable=True, comment='埋点数据'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False, comment='更新时间'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('user_activity_log')
