"""initial migration

Revision ID: 3d6b9ae59bfc
Revises: 1cfb4e3f6c6c
Create Date: 2015-07-15 07:07:32.984000

"""

# revision identifiers, used by Alembic.
revision = '3d6b9ae59bfc'
down_revision = '1cfb4e3f6c6c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('body_html', sa.Text(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'body_html')
    ### end Alembic commands ###
