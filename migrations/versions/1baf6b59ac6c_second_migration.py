"""Second Migration

Revision ID: 1baf6b59ac6c
Revises: 1af2ccf1d325
Create Date: 2021-05-07 21:45:51.498528

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1baf6b59ac6c'
down_revision = '1af2ccf1d325'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('comments', 'post_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('comments', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('comments', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('comments', 'post_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
