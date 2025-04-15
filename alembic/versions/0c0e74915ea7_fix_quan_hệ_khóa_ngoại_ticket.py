"""Fix quan hệ khóa ngoại Ticket

Revision ID: 0c0e74915ea7
Revises: 7a3db707d230
Create Date: 2025-04-09 09:50:22.928900

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c0e74915ea7'
down_revision: Union[str, None] = '7a3db707d230'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'ticket', 'room', ['id_room'], ['id_room'], onupdate='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'ticket', type_='foreignkey')
    # ### end Alembic commands ###
