"""added cascading behaviour to user-post relationship

Revision ID: 46d0ebbceb5e
Revises: 9adea9861ace
Create Date: 2026-09-10 13:29:35.713177

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "46d0ebbceb5e"
down_revision: Union[str, Sequence[str], None] = "9adea9861ace"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("posts") as batch_op:
        batch_op.create_foreign_key("fk_user_id", "users", ["user_id"], ["id"], ondelete="CASCADE")


def downgrade() -> None:
    with op.batch_alter_table("posts") as batch_op:
        batch_op.create_foreign_key("user_id", "users", ["user_id"], ["id"])
