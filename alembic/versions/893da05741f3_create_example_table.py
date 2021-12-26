"""create example table

Revision ID: 893da05741f3
Revises: 38383f7f9ba5
Create Date: 2020-03-08 12:21:02.364125

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '893da05741f3'
down_revision = '38383f7f9ba5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'example',

        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column(
            "owner", sa.Integer, sa.ForeignKey('user.id'), nullable=False
        ),
        sa.Column('message', sa.String(256), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
    )


def downgrade():
    op.drop_table('example')
