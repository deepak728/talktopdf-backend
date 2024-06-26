"""uploadedPdf

Revision ID: 88a997d07701
Revises: 
Create Date: 2023-09-12 02:20:55.149144

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "88a997d07701"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "uploaded_pdf",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("path", sa.String(length=255), nullable=False),
        sa.UniqueConstraint("path", name="unique_path_constraint"),
    )

    op.create_table(
        "chunks",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("pdf_id", sa.Integer, nullable=False),
        sa.Column("chunk", sa.Text, nullable=True),
        sa.ForeignKeyConstraint(
            ["pdf_id"], ["uploaded_pdf.id"], name="fk_chunks_pdf_id"
        ),
    )


def downgrade():
    op.drop_table("chunks")
    op.drop_table("uploaded_pdf")
