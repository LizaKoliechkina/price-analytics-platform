"""create product table

Revision ID: 9f2bd395b8ac
Revises: 
Create Date: 2023-08-03 23:16:29.315509

"""
from uuid import uuid4

from alembic import op
from sqlalchemy import Column, String, Float, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '9f2bd395b8ac'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'product',
        Column('id', UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4().hex),
        Column('name', String(length=100), nullable=False),
        Column('description', String(length=300), nullable=True),
        Column('global_price', Float, nullable=False),
        Column('local_price', Float, nullable=False),
        Column('sold_quantity', Integer, nullable=False),
        Column('cluster', String(length=50), nullable=False),
        Column('division', String(length=50), nullable=False),
        Column('country', String(length=50), nullable=False),
        UniqueConstraint('name', 'cluster', 'division', 'country')
    )


def downgrade() -> None:
    op.drop_table('product')
