"""init

Revision ID: 4494d29898c5
Revises: 
Create Date: 2023-10-31 12:11:40.657551

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4494d29898c5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('link_trailer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_film', sa.Text(), nullable=True),
    sa.Column('link_trailer', sa.Text(), nullable=True),
    sa.Column('status', sa.Text(), nullable=True),
    sa.Column('date_update', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('link_trailer')
    # ### end Alembic commands ###
