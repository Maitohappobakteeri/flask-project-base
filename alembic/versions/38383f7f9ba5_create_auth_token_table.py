"""create auth token table

Revision ID: 38383f7f9ba5
Revises: 48a006fa9cf8
Create Date: 2020-03-21 17:19:43.765313

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38383f7f9ba5'
down_revision = '48a006fa9cf8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'auth_token',

        sa.Column('jti', sa.CHAR(37), primary_key=True),
        sa.Column(
            "owner", sa.Integer, sa.ForeignKey('user.id'), nullable=False
        ),
        sa.Column('access', sa.Boolean, nullable=False),
        sa.Column('expires_at', sa.DateTime, nullable=False),
        sa.Column("client", sa.Integer, nullable=False),
    )


def downgrade():
    op.drop_table('auth_token')
