"""Initial migration

Revision ID: 5ee10e4e06ed
Revises: 
Create Date: 2021-06-13 21:33:26.411397

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ee10e4e06ed'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('player_salary',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('player_name', sa.String(length=100), nullable=True),
    sa.Column('salary', sa.Integer(), nullable=True),
    sa.Column('season_start', sa.Integer(), nullable=True),
    sa.Column('season_end', sa.Integer(), nullable=True),
    sa.Column('team_short', sa.String(length=10), nullable=True),
    sa.Column('team_full', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('player_stats',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('player_name', sa.String(length=100), nullable=True),
    sa.Column('season', sa.Integer(), nullable=True),
    sa.Column('position', sa.String(length=100), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('team', sa.String(length=100), nullable=True),
    sa.Column('games_played', sa.Integer(), nullable=True),
    sa.Column('games_started', sa.Integer(), nullable=True),
    sa.Column('min_played', sa.Integer(), nullable=True),
    sa.Column('per', sa.Float(), nullable=True),
    sa.Column('true_shooting', sa.Float(), nullable=True),
    sa.Column('three_pt_att_rate', sa.Float(), nullable=True),
    sa.Column('ft_rate', sa.Float(), nullable=True),
    sa.Column('off_reb_perc', sa.Float(), nullable=True),
    sa.Column('def_reb_perc', sa.Float(), nullable=True),
    sa.Column('total_reb_perc', sa.Float(), nullable=True),
    sa.Column('assist_perc', sa.Float(), nullable=True),
    sa.Column('steal_perc', sa.Float(), nullable=True),
    sa.Column('block_perc', sa.Float(), nullable=True),
    sa.Column('to_perc', sa.Float(), nullable=True),
    sa.Column('usage_perc', sa.Float(), nullable=True),
    sa.Column('offensive_win_shares', sa.Float(), nullable=True),
    sa.Column('defensive_win_shares', sa.Float(), nullable=True),
    sa.Column('win_shares', sa.Float(), nullable=True),
    sa.Column('win_shares_per_48', sa.Float(), nullable=True),
    sa.Column('offensive_box_p_m', sa.Float(), nullable=True),
    sa.Column('defensive_box_p_m', sa.Float(), nullable=True),
    sa.Column('box_p_m', sa.Float(), nullable=True),
    sa.Column('var', sa.Float(), nullable=True),
    sa.Column('fg', sa.Float(), nullable=True),
    sa.Column('fga', sa.Integer(), nullable=True),
    sa.Column('fg_perc', sa.Float(), nullable=True),
    sa.Column('three_pt_fg', sa.Integer(), nullable=True),
    sa.Column('three_pt_fga', sa.Integer(), nullable=True),
    sa.Column('three_pt_fg_perc', sa.Float(), nullable=True),
    sa.Column('two_pt_fg', sa.Integer(), nullable=True),
    sa.Column('two_pt_fga', sa.Float(), nullable=True),
    sa.Column('two_pt_fg_perc', sa.Float(), nullable=True),
    sa.Column('effective_fg_perc', sa.Float(), nullable=True),
    sa.Column('ft', sa.Integer(), nullable=True),
    sa.Column('fta', sa.Integer(), nullable=True),
    sa.Column('ft_perc', sa.Float(), nullable=True),
    sa.Column('off_reb', sa.Integer(), nullable=True),
    sa.Column('def_reb', sa.Integer(), nullable=True),
    sa.Column('reb', sa.Integer(), nullable=True),
    sa.Column('assists', sa.Integer(), nullable=True),
    sa.Column('steals', sa.Integer(), nullable=True),
    sa.Column('blocks', sa.Integer(), nullable=True),
    sa.Column('turnovers', sa.Integer(), nullable=True),
    sa.Column('fouls', sa.Integer(), nullable=True),
    sa.Column('points', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('player_stats')
    op.drop_table('player_salary')
    # ### end Alembic commands ###
