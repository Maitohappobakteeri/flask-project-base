"""create user table

Revision ID: 48a006fa9cf8
Revises:
Create Date: 2020-03-08 02:54:39.052730

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48a006fa9cf8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(64), nullable=False),
        sa.Column('password', sa.String(256), nullable=False),
    )


def downgrade():
    op.drop_table('user')
