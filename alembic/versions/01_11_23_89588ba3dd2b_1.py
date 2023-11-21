"""1

Revision ID: 89588ba3dd2b
Revises: c8d3c77b2486
Create Date: 2023-11-01 17:23:37.587608

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '89588ba3dd2b'
down_revision: Union[str, None] = 'c8d3c77b2486'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('link_trailer', 'date_update',
                    existing_type=postgresql.TIMESTAMP(),
                    type_=sa.String(),
                    existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('link_trailer', 'date_update',
                    existing_type=sa.String(),
                    type_=postgresql.TIMESTAMP(),
                    existing_nullable=True)
    # ### end Alembic commands ###
