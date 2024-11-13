from functools import wraps
import random
import streamlit as st
import altair as alt

GOOD_COLOR = '#007BB9'
EVIL_COLOR = '#8C0E12'
TB_COLOR = '#880004'
BMR_COLOR = '#D87C22'
SNV_COLOR = '#642195'
OTHER_COLOR = '#999999'
OTHER_COLORS = ['#243D8B', '#24858B', '#8B2477', '#248B3C', '#CF56DA']

PARAMETER_TO_COLUMN_MAP = {
        "Skript": "script",
        "Spieleranzahl": "playercount",
         "Erzähler": "storyteller"
}

def valid_chart_check(chart_function):
    @wraps(chart_function)
    def function_wrapper(df, *args, **kwargs):

        if df.empty:
            return
        return chart_function(df, *args, **kwargs)
    return function_wrapper

################################################### GAME CHARTS #################################################################################
@valid_chart_check
def create_bar_chart(df):
    # df['date'] = pd.to_datetime(df['formatted_date'])
    win_counts = df.groupby(['formatted_date', 'win']).size().reset_index(name='win_count')
    pivot_df = win_counts.pivot(index='formatted_date', columns='win', values='win_count').fillna(0).reset_index()
    if len(pivot_df.columns.tolist()[1:]) != 2:
        return
    st.bar_chart(pivot_df, x='formatted_date', y=pivot_df.columns.tolist()[1:], color=[EVIL_COLOR,GOOD_COLOR], x_label="Datum", y_label="Siege")

@valid_chart_check
def create_script_line_chart(df):
    # Other: Total plays < 8
    other_threshold = 8
    overall_count = df.groupby(["script"]).size()
    other_scripts = overall_count[overall_count < other_threshold].index.tolist()
    df['script'] = df['script'].apply(lambda x: 'Other' if x in other_scripts else x)
    script_counts = df.groupby(['formatted_date', 'script']).size().reset_index(name='script_count')
    colors = []
    i = 0
    pivot_df = script_counts.pivot(index='formatted_date', columns='script', values='script_count').fillna(0).reset_index()
    
    for column in pivot_df.columns.tolist()[1:]:
        if column == 'TB':
            colors.append(TB_COLOR)
        elif column == 'BMR':
            colors.append(BMR_COLOR)
        elif column == 'SNV':
            colors.append(SNV_COLOR)
        elif column == 'Other':
            colors.append(OTHER_COLOR)
        else:
            if i < 5:
                colors.append(OTHER_COLORS[i])
                i+=1
            else:
                colors.append("%06x" % random.randint(0, 0xFFFFFF))

    st.bar_chart(pivot_df, x="formatted_date", y=pivot_df.columns.tolist()[1:], color=colors, x_label="Datum", y_label="Spielanzahl")

@valid_chart_check
def create_winrate_over_time_chart(df):
    # Step 1: Group by 'date' and 'winner' to get the count of wins for each team
    win_counts = df.groupby(['formatted_date', 'win']).size().unstack(fill_value=0).reset_index()

    # Step 2: Calculate cumulative wins for each team
    win_counts['good_cumulative'] = win_counts['Gut'].cumsum()
    win_counts['evil_cumulative'] = win_counts['Böse'].cumsum()

    # Step 3: Calculate total games played up to each date
    win_counts['total_games'] = win_counts['good_cumulative'] + win_counts['evil_cumulative']

    # Step 4: Calculate cumulative win rate for each team
    win_counts['good_rate'] = win_counts['good_cumulative'] / win_counts['total_games']
    win_counts['evil_rate'] = win_counts['evil_cumulative'] / win_counts['total_games']
    st.line_chart(win_counts, x="formatted_date", y=["good_rate", "evil_rate"], color=[EVIL_COLOR,GOOD_COLOR], x_label="Datum", y_label="Winrate")

@valid_chart_check
def create_grouped_winrate_chart(df, column):
    column = PARAMETER_TO_COLUMN_MAP[column]
    grouped_wins = df.groupby([column, 'win']).size().unstack(fill_value=0).reset_index()
    st.bar_chart(grouped_wins, x=column, y=["Böse", "Gut"], color=[EVIL_COLOR, GOOD_COLOR], stack="normalize")

@valid_chart_check
def create_gamecount_charts(df, column):
    column = PARAMETER_TO_COLUMN_MAP[column]
    grouped_wins = df.groupby([column]).size().reset_index(name="game_count")
    st.bar_chart(grouped_wins, x=column, y="game_count")

@valid_chart_check
def create_playercount_over_time_chart(df):
    player_count_df = df.groupby('formatted_date')['playercount'].max().reset_index()
    st.line_chart(player_count_df, x="formatted_date", y="playercount", x_label="Datum", y_label="Maximale Spieleranzahl")


################################################### ROLE CHARTS #################################################################################
@valid_chart_check
def create_role_bar_chart(df, column):
    column = PARAMETER_TO_COLUMN_MAP[column] if column in PARAMETER_TO_COLUMN_MAP else column
    role_count = df.groupby([column]).size().reset_index(name='game_count')
    st.bar_chart(role_count, x=column, y="game_count", x_label=column, y_label="Vorkommen")



@valid_chart_check
def create_role_winrate_chart(df, column):
    column = PARAMETER_TO_COLUMN_MAP[column] if column in PARAMETER_TO_COLUMN_MAP else column
    grouped_wins = df.groupby([column, 'player_result']).size().unstack(fill_value=0).reset_index()
    st.bar_chart(grouped_wins, x=column, y=["Win", "Loss"], color=[EVIL_COLOR, GOOD_COLOR], stack="normalize")

@valid_chart_check
def create_role_rolling_winrate_chart(df):
        # Step 1: Group by 'date' and 'winner' to get the count of wins for each team
    win_counts = df.groupby(['formatted_date', 'player_result']).size().unstack(fill_value=0).reset_index()

    # Step 2: Calculate cumulative wins for each team
    win_counts['win_cumulative'] = win_counts['Win'].cumsum()
    win_counts['loss_cumulative'] = win_counts['Loss'].cumsum()

    # Step 3: Calculate total games played up to each date
    win_counts['total_games'] = win_counts['win_cumulative'] + win_counts['loss_cumulative']

    # Step 4: Calculate cumulative win rate for each team
    win_counts['win_rate'] = win_counts['win_cumulative'] / win_counts['total_games']
    win_counts['loss_rate'] = win_counts['loss_cumulative'] / win_counts['total_games']
    st.line_chart(win_counts, x="formatted_date", y="win_rate", color=[GOOD_COLOR], x_label="Datum", y_label="Winrate")


################################################### PLAYER CHARTS ######################

# Define a function to apply background colors based on 'player_result'
def highlight_player_result(row):
    color = '#248B3C' if row['player_result'] == 'Win' else '#999999'  # Light blue for Win, grey for Loss
    color_team = GOOD_COLOR if row['team'] == 'Gut' else EVIL_COLOR  # Light blue for Win, grey for Loss
    styles = []
    for col in row.index:
        if col == "player_result":
            styles.append(f'background-color: {color}')
        elif col == "team":
            styles.append(f'background-color: {color_team}')
        else:
            styles.append('')
    return styles

@valid_chart_check
def create_winrate_over_time_chart_player(df):
    # Add new columns based on team and player_result
    df['good_team_win'] = ((df['team'] == "Gut") & (df['player_result'] == 'Win')).astype(int)
    df['evil_team_win'] = ((df['team'] == "Böse") & (df['player_result'] == 'Win')).astype(int)
    df['good_team_game'] = (df['team'] == "Gut").astype(int)
    df['evil_team_game'] = (df['team'] == "Böse").astype(int)
    df['win'] = (df['player_result'] == 'Win').astype(int)
    df['game'] = 1  # Each row represents a game

    df = df.groupby('formatted_date').agg(
            good_team_win=('good_team_win', 'sum'),
            evil_team_win=('evil_team_win', 'sum'),
            good_team_game=('good_team_game', 'sum'),
            evil_team_game=('evil_team_game', 'sum'),
            win=('win', 'sum'),
            game=('game', 'sum')
        ).reset_index()
    # Calculate cumulative sums
    df['cumulative_good_team_wins'] = df['good_team_win'].cumsum()
    df['cumulative_evil_team_wins'] = df['evil_team_win'].cumsum()
    df['cumulative_good_team_games'] = df['good_team_game'].cumsum()
    df['cumulative_evil_team_games'] = df['evil_team_game'].cumsum()
    df['cumulative_wins'] = df['win'].cumsum()
    df['cumulative_games'] = df['game'].cumsum()

    df["good_win_rate"] = df["cumulative_good_team_wins"]/df["cumulative_good_team_games"]
    df["evil_win_rate"] = df["cumulative_evil_team_wins"]/df["cumulative_evil_team_games"]
    df["win_rate"] = df["cumulative_wins"]/df["cumulative_games"]

    # Final dataframe with only the desired columns
    result_df = df[['formatted_date', "good_win_rate", "evil_win_rate", "win_rate"]]
    st.line_chart(result_df, x="formatted_date", y=["good_win_rate", "evil_win_rate", "win_rate"], color=[EVIL_COLOR,GOOD_COLOR, '#248B3C'], x_label="Datum", y_label="Winrate")

@valid_chart_check
def create_player_role_dist_chart(df):
    df = df.groupby('role').agg(
        number_of_games=('player_result', 'size'),
        number_of_wins=('player_result', lambda x: (x == 'Win').sum())
    ).reset_index()

    df["number_of_losses"] = df["number_of_games"] - df["number_of_wins"]

    st.bar_chart(data= df, x="role", y=["number_of_wins", "number_of_losses"], color=['#999999','#248B3C'])