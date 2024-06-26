"""Initial migration

Revision ID: c59da6ef81c2
Revises: 
Create Date: 2024-02-29 12:01:46.835654

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c59da6ef81c2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Customers',
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('GivenName', sa.String(length=50), nullable=False),
    sa.Column('Surname', sa.String(length=50), nullable=False),
    sa.Column('Streetaddress', sa.String(length=50), nullable=False),
    sa.Column('City', sa.String(length=50), nullable=False),
    sa.Column('Zipcode', sa.String(length=10), nullable=False),
    sa.Column('Country', sa.String(length=30), nullable=False),
    sa.Column('CountryCode', sa.String(length=2), nullable=False),
    sa.Column('NationalId', sa.String(length=20), nullable=False),
    sa.Column('Telephone', sa.String(length=20), nullable=False),
    sa.Column('EmailAddress', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('Id')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('password', sa.String(length=100), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('fs_uniquifier', sa.String(length=255), nullable=False),
    sa.Column('confirmed_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('fs_uniquifier')
    )
    op.create_table('Accounts',
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('AccountType', sa.String(length=10), nullable=False),
    sa.Column('Created', sa.DateTime(), nullable=False),
    sa.Column('Balance', sa.Float(), nullable=False),
    sa.Column('CustomerId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['CustomerId'], ['Customers.Id'], ),
    sa.PrimaryKeyConstraint('Id')
    )
    op.create_table('roles_users',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('Transactions',
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('Type', sa.String(length=20), nullable=False),
    sa.Column('Operation', sa.String(length=50), nullable=False),
    sa.Column('Date', sa.DateTime(), nullable=False),
    sa.Column('Amount', sa.Float(), nullable=False),
    sa.Column('NewBalance', sa.Float(), nullable=False),
    sa.Column('AccountId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['AccountId'], ['Accounts.Id'], ),
    sa.PrimaryKeyConstraint('Id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Transactions')
    op.drop_table('roles_users')
    op.drop_table('Accounts')
    op.drop_table('user')
    op.drop_table('role')
    op.drop_table('Customers')
    # ### end Alembic commands ###
