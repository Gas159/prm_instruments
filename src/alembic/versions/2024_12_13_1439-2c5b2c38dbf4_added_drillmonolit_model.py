"""added DrillMonolit model

Revision ID: 2c5b2c38dbf4
Revises: efce815cee5e
Create Date: 2024-12-13 14:39:36.815280

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2c5b2c38dbf4"
down_revision: Union[str, None] = "efce815cee5e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "drill_monolit",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("material", sa.String(), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("diameter", sa.Float(), nullable=True),
        sa.Column("length_xD", sa.Float(), nullable=True),
        sa.Column("deep_of_drill", sa.Float(), nullable=True),
        sa.Column("coating", sa.String(), nullable=True),
        sa.Column("count", sa.Integer(), nullable=True),
        sa.Column("count_min", sa.Integer(), nullable=True),
        sa.Column("company", sa.String(), nullable=True),
        sa.Column("storage", sa.String(), nullable=True),
        sa.Column("is_broken", sa.Boolean(), nullable=True),
        sa.Column("image_path", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column(
            "create_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "update_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_drill_monolit")),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("drill_monolit")
    # ### end Alembic commands ###