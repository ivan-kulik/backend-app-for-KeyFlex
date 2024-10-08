"""delete touch typing in profiles table

Revision ID: 45d549ecfb42
Revises: d81f751ad06e
Create Date: 2024-08-18 21:34:51.330102

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "45d549ecfb42"
down_revision: Union[str, None] = "d81f751ad06e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("profiles", "touch_typing")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "profiles",
        sa.Column(
            "touch_typing", sa.VARCHAR(), autoincrement=False, nullable=True
        ),
    )
    # ### end Alembic commands ###
