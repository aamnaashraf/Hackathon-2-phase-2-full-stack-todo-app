"""Add priority column to todos table

Revision ID: 001
Revises:
Create Date: 2025-12-25 12:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the priority enum type
    priority_enum = postgresql.ENUM('low', 'medium', 'high', name='priority_enum', create_type=False)
    priority_enum.create(op.get_bind(), checkfirst=True)

    # Add the priority column to the todos table
    op.add_column('todo', sa.Column('priority', priority_enum, server_default='medium', nullable=True))


def downgrade() -> None:
    # Drop the priority column
    op.drop_column('todo', 'priority')

    # Drop the enum type
    op.execute("DROP TYPE IF EXISTS priority_enum;")