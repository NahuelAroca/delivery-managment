"""seed drivers

Revision ID: 7555786de795
Revises: 0765b8295206
Create Date: 2026-09-14 00:57:13.383764

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7555786de795'
down_revision: Union[str, Sequence[str], None] = '0765b8295206'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("INSERT INTO drivers (name) VALUES ('Driver 1'), ('Driver 2'), ('Driver 3'), ('Driver 4')")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DELETE FROM drivers WHERE name IN ('Driver 1', 'Driver 2', 'Driver 3', 'Driver 4')")
