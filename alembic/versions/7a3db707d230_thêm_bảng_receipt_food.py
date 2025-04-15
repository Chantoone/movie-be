"""Thêm bảng receipt_food

Revision ID: 7a3db707d230
Revises: abe3836ae318
Create Date: 2025-04-09 09:06:27.317979

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7a3db707d230'
down_revision: Union[str, None] = 'abe3836ae318'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('receipt_food',
    sa.Column('id_receipt', sa.Integer(), nullable=False),
    sa.Column('id_food', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_food'], ['food.id_food'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['id_receipt'], ['receipt.id_receipt'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id_receipt', 'id_food')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('receipt_food')
    # ### end Alembic commands ###
