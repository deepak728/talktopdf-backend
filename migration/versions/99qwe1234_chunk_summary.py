"""Add chunk_summary table

Revision ID: new_revision_id
Revises: previous_revision_id
Create Date: 2024-05-19 02:20:55.149144

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "99qwe1234"
down_revision = "88a997d07701"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "chunk_summary",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("pdf_id", sa.Integer, nullable=False),
        sa.Column("chunk_id", sa.Integer, nullable=False),
        sa.Column("summary", sa.Text, nullable=True),
        sa.ForeignKeyConstraint(
            ["pdf_id"], ["uploaded_pdf.id"], name="fk_chunk_summary_pdf_id"
        ),
        sa.ForeignKeyConstraint(
            ["chunk_id"], ["chunks.id"], name="fk_chunk_summary_chunk_id"
        ),
    )


def downgrade():
    op.drop_table("chunk_summary")
