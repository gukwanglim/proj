"""empty message

Revision ID: eecf4a197b24
Revises: be75bb0c93d0
Create Date: 2022-07-28 11:40:38.600954

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eecf4a197b24'
down_revision = 'be75bb0c93d0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product',
    sa.Column('prod_id', sa.Integer(), nullable=False),
    sa.Column('prod_image', sa.String(length=800), nullable=False),
    sa.Column('prod_name', sa.String(length=150), nullable=False),
    sa.Column('prod_price', sa.String(length=150), nullable=False),
    sa.Column('prod_quantity', sa.String(length=150), nullable=True),
    sa.Column('prod_expand', sa.String(length=300), nullable=False),
    sa.PrimaryKeyConstraint('prod_id'),
    sa.UniqueConstraint('prod_expand'),
    sa.UniqueConstraint('prod_image'),
    sa.UniqueConstraint('prod_name'),
    sa.UniqueConstraint('prod_price')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product')
    # ### end Alembic commands ###
