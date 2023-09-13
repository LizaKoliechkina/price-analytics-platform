"""Add cluster table

Revision ID: e349512e66c3
Revises: f0a0992248c9
Create Date: 2023-09-11 15:48:20.797850

"""
from alembic import op
from sqlalchemy import Column, String, Integer, text
from sqlalchemy.orm import declarative_base, Session


# revision identifiers, used by Alembic.
revision = 'e349512e66c3'
down_revision = 'f0a0992248c9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'cluster',
        Column('name', String(length=50), primary_key=True, nullable=False),
        Column('description', String(length=300), nullable=True),
        Column('division', String(length=50), nullable=False),
        Column(
            'previous_sold_quantity',
            Integer,
            nullable=False,
            server_default=text('0'),
        )
    )

    op.execute(
        'INSERT INTO cluster (name, division) '
        'SELECT DISTINCT cluster, division FROM product'
    )
    op.drop_column('product', 'division')
    op.create_foreign_key('fk_product_cluster', 'product', 'cluster', ['cluster'], ['name'])
    op.create_unique_constraint(
        'uc_product_cluster_country',
        'product',
        ['name', 'cluster', 'country'],
    )


Base = declarative_base()


class Cluster(Base):
    __tablename__ = 'cluster'
    name = Column(String(length=50), primary_key=True, nullable=False)
    division = Column(String(length=50), nullable=False)


def downgrade() -> None:
    op.add_column(
        'product',
        Column('division', String(length=50), nullable=False, server_default='temp'),
    )

    bind = op.get_bind()
    session = Session(bind)
    clusters = session.query(Cluster).all()
    for clust in clusters:
        op.execute(
            f"UPDATE product SET division = '{clust.division}' "
            f"WHERE cluster = '{clust.name}';"
        )

    op.drop_constraint('fk_product_cluster', 'product')
    op.drop_table('cluster')
    op.drop_constraint('uc_product_cluster_country', 'product')
    op.create_unique_constraint(
        'uc_product_cluster_division_country',
        'product',
        ['name', 'cluster', 'division', 'country'],
    )
