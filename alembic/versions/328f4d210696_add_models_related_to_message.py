"""add models related to message

Revision ID: 328f4d210696
Revises: b1d890c1353c
Create Date: 2025-07-09 16:07:33.284856

"""

from typing import Sequence
from typing import Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "328f4d210696"
down_revision: Union[str, None] = "b1d890c1353c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "messages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("sender_id", sa.String(length=50), nullable=True),
        sa.Column("receiver_id", sa.String(length=50), nullable=True),
        sa.Column("content", sa.Text(), nullable=True),
        sa.Column("message_type", sa.String(length=20), nullable=True),
        sa.Column("is_read", sa.Boolean(), nullable=True),
        sa.Column("meta", sa.Text(), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, comment="创建时间"),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False, comment="更新时间"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_messages_receiver_id"), "messages", ["receiver_id"], unique=False)
    op.create_index(op.f("ix_messages_sender_id"), "messages", ["sender_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_messages_sender_id"), table_name="messages")
    op.drop_index(op.f("ix_messages_receiver_id"), table_name="messages")
    op.drop_table("messages")
