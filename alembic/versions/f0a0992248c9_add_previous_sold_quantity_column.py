"""Add previous_sold_quantity column

Revision ID: f0a0992248c9
Revises: 9f2bd395b8ac
Create Date: 2023-08-18 00:48:41.235535

"""
from alembic import op
from sqlalchemy import Column, Integer, text

# revision identifiers, used by Alembic.
revision = 'f0a0992248c9'
down_revision = '9f2bd395b8ac'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'product',
        Column(
            'previous_sold_quantity',
            Integer,
            nullable=False,
            server_default=text('0'),
        )
    )


def downgrade() -> None:
    op.drop_column('product', 'previous_sold_quantity')
