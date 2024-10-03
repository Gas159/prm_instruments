"""reafact

Revision ID: 016553ef8e1c
Revises: 107c9a42a0cf
Create Date: 2024-10-03 23:36:16.053049

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "016553ef8e1c"
down_revision: Union[str, None] = "107c9a42a0cf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("drill", sa.Column("key_", sa.String(), nullable=True))
    op.drop_column("drill", "key")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "drill",
        sa.Column("key", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.drop_column("drill", "key_")
    # ### end Alembic commands ###