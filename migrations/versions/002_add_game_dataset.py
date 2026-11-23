"""Add GameHub datasets and their CSV file records."""

import sqlalchemy as sa
from alembic import op

revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "game_dataset",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("ds_meta_data_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"]),
        sa.ForeignKeyConstraint(["ds_meta_data_id"], ["ds_meta_data.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "game_dataset_file",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("game_dataset_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("checksum", sa.String(length=120), nullable=False),
        sa.Column("size", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["game_dataset_id"], ["game_dataset.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("game_dataset_file")
    op.drop_table("game_dataset")
