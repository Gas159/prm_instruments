"""add table plate

Revision ID: 107c9a42a0cf
Revises: d9c13cd53070
Create Date: 2024-10-03 14:46:06.917762

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "107c9a42a0cf"
down_revision: Union[str, None] = "d9c13cd53070"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "plate",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("type", sa.String(), nullable=True),
        sa.Column("sub_type", sa.String(), nullable=True),
        sa.Column(
            "material",
            sa.Enum("S", "M", "P", name="materialenum"),
            nullable=True,
        ),
        sa.Column("amount", sa.Integer(), nullable=True),
        sa.Column("min_amount", sa.Integer(), nullable=True),
        sa.Column("company", sa.String(), nullable=True),
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
        sa.PrimaryKeyConstraint("id", name=op.f("pk_plate")),
    )
    op.create_table(
        "drill_plate_association",
        sa.Column("drill_id", sa.Integer(), nullable=False),
        sa.Column("plate_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["drill_id"],
            ["drill.id"],
            name=op.f("fk_drill_plate_association_drill_id_drill"),
        ),
        sa.ForeignKeyConstraint(
            ["plate_id"],
            ["plate.id"],
            name=op.f("fk_drill_plate_association_plate_id_plate"),
        ),
        sa.PrimaryKeyConstraint("drill_id", "plate_id", name=op.f("pk_drill_plate_association")),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("drill_plate_association")
    op.drop_table("plate")
    # ### end Alembic commands ###
