"""change foreign key for profiles table

Revision ID: a52df1e7724f
Revises: d3cfd5e23aac
Create Date: 2024-08-18 16:34:07.158640

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a52df1e7724f"
down_revision: Union[str, None] = "d3cfd5e23aac"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "profiles",
        sa.Column("user_reference", sa.String(length=20), nullable=False),
    )
    op.drop_constraint("uq_profiles_user_id", "profiles", type_="unique")
    op.create_unique_constraint(
        op.f("uq_profiles_user_reference"), "profiles", ["user_reference"]
    )
    op.drop_constraint(
        "fk_profiles_user_id_users", "profiles", type_="foreignkey"
    )
    op.create_foreign_key(
        op.f("fk_profiles_user_reference_users"),
        "profiles",
        "users",
        ["user_reference"],
        ["username"],
    )
    op.drop_column("profiles", "user_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "profiles",
        sa.Column(
            "user_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
    )
    op.drop_constraint(
        op.f("fk_profiles_user_reference_users"),
        "profiles",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "fk_profiles_user_id_users", "profiles", "users", ["user_id"], ["id"]
    )
    op.drop_constraint(
        op.f("uq_profiles_user_reference"), "profiles", type_="unique"
    )
    op.create_unique_constraint("uq_profiles_user_id", "profiles", ["user_id"])
    op.drop_column("profiles", "user_reference")
    # ### end Alembic commands ###
