"""Init project

Revision ID: 0fd73486442b
Revises: 
Create Date: 2025-03-09 14:58:00.442401

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0fd73486442b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('teachers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=False),
    sa.Column('last_name', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('phone', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('students',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=False),
    sa.Column('last_name', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('phone', sa.String(length=30), nullable=True),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('subjects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('teacher_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['teacher_id'], ['teachers.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('grades',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('subject_id', sa.Integer(), nullable=False),
    sa.Column('grade', sa.Float(), nullable=False),
    sa.Column('date_received', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['subject_id'], ['subjects.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('grades')
    op.drop_table('subjects')
    op.drop_table('students')
    op.drop_table('teachers')
    op.drop_table('groups')
    # ### end Alembic commands ###
