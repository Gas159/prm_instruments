"""upd table

Revision ID: 1b18e6eb5a5b
Revises: 6a5b30fb9615
Create Date: 2024-08-26 15:43:15.437992

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "1b18e6eb5a5b"
down_revision: Union[str, None] = "6a5b30fb9615"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_user_email", table_name="user")
    op.drop_table("user")
    op.drop_table("service")
    op.drop_table("company")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "company",
        sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column(
            "description", sa.VARCHAR(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "coordinates", sa.VARCHAR(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "id",
            sa.INTEGER(),
            server_default=sa.text("nextval('company_id_seq'::regclass)"),
            autoincrement=True,
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name="pk_company"),
        postgresql_ignore_search_path=False,
    )
    op.create_table(
        "service",
        sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column(
            "description", sa.VARCHAR(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "company_id", sa.INTEGER(), autoincrement=False, nullable=True
        ),
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(
            ["company_id"],
            ["company.id"],
            name="fk_service_company_id_company",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_service"),
    )
    op.create_table(
        "user",
        sa.Column(
            "username", sa.VARCHAR(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "second_name", sa.VARCHAR(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "email",
            sa.VARCHAR(length=320),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "registration_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "hashed_password",
            sa.VARCHAR(length=1024),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "is_active", sa.BOOLEAN(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "is_superuser", sa.BOOLEAN(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "is_verified", sa.BOOLEAN(), autoincrement=False, nullable=False
        ),
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_user"),
    )
    op.create_index("ix_user_email", "user", ["email"], unique=True)
    # ### end Alembic commands ###
