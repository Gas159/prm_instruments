"""add new column

Revision ID: 234a58cd44e8
Revises: 824970e6c6e4
Create Date: 2024-09-24 21:23:05.836696

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "234a58cd44e8"
down_revision: Union[str, None] = "824970e6c6e4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("tool", sa.Column("plate", sa.String(), nullable=True))
    op.add_column("tool", sa.Column("screws", sa.String(), nullable=True))
    op.add_column("tool", sa.Column("key", sa.String(), nullable=True))
    op.add_column("tool", sa.Column("company", sa.String(), nullable=True))
    op.alter_column(
        "tool",
        "lenght",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=True,
    )
    op.alter_column(
        "tool",
        "deep_of_drill",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=True,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "tool",
        "deep_of_drill",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=False,
    )
    op.alter_column(
        "tool",
        "lenght",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=False,
    )
    op.drop_column("tool", "company")
    op.drop_column("tool", "key")
    op.drop_column("tool", "screws")
    op.drop_column("tool", "plate")
    # ### end Alembic commands ###
