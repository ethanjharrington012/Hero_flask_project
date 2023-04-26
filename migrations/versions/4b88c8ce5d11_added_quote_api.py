"""added quote api

Revision ID: 4b88c8ce5d11
Revises: e02005fd7b6a
Create Date: 2023-04-25 15:56:52.108666

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b88c8ce5d11'
down_revision = 'e02005fd7b6a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('hero', schema=None) as batch_op:
        batch_op.add_column(sa.Column('random_marvel', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('hero', schema=None) as batch_op:
        batch_op.drop_column('random_marvel')

    # ### end Alembic commands ###
