#!/usr/bin/env python3
import sys, json, os, warnings
warnings.filterwarnings('ignore')
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

def load_and_train():
    teams   = pd.read_csv(os.path.join(DATA_DIR, 'all_teams_data.csv'))
    matches = pd.read_csv(os.path.join(DATA_DIR, 'all_ipl_matches_data.csv'))

    t_map = dict(zip(teams['team_id'], teams['team_name']))
    for col in ['team1','team2','toss_winner','match_winner']:
        matches[col] = matches[col].map(t_map)
    matches['season'] = matches['season'].astype(str).str.replace('/21','').astype(int)

    df = matches[matches['result']=='win'].copy().dropna(subset=['match_winner','team1','team2'])

    win_rate = {}
    for team in df['team1'].dropna().unique():
        played = len(df[(df['team1']==team)|(df['team2']==team)])
        won    = len(df[df['match_winner']==team])
        win_rate[team] = won/played if played > 0 else 0.5

    df['team1_wr']    = df['team1'].map(win_rate).fillna(0.5)
    df['team2_wr']    = df['team2'].map(win_rate).fillna(0.5)
    df['toss_home']   = (df['toss_winner']==df['team1']).astype(int)
    df['field_first'] = (df['toss_decision']=='field').astype(int)

    le_team = LabelEncoder()
    le_team.fit(pd.concat([df['team1'],df['team2'],df['match_winner']]).dropna().unique())
    df['t1_enc']     = le_team.transform(df['team1'])
    df['t2_enc']     = le_team.transform(df['team2'])
    le_v = LabelEncoder()
    df['venue_enc']  = le_v.fit_transform(df['venue'].fillna('Unknown'))
    df['winner_enc'] = le_team.transform(df['match_winner'])

    features = ['t1_enc','t2_enc','team1_wr','team2_wr','toss_home','field_first','venue_enc','season']
    X = df[features]; y = df['winner_enc']
    X_train, X_test, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    rf = RandomForestClassifier(n_estimators=300, max_depth=10, random_state=42)
    rf.fit(X_train, y_train)

    return rf, le_team, le_v, win_rate

def predict(params):
    rf, le_team, le_v, win_rate = load_and_train()

    team1        = params['team1']
    team2        = params['team2']
    toss_winner  = params['tossWinner']
    toss_decision= params['tossDecision']
    venue        = params['venue']
    season       = int(params['season'])

    t1_wr = win_rate.get(team1, 0.5)
    t2_wr = win_rate.get(team2, 0.5)
    toss_home   = 1 if toss_winner == team1 else 0
    field_first = 1 if toss_decision == 'field' else 0

    t1_enc = int(le_team.transform([team1])[0]) if team1 in le_team.classes_ else 0
    t2_enc = int(le_team.transform([team2])[0]) if team2 in le_team.classes_ else 0
    v_enc  = int(le_v.transform([venue])[0])    if venue  in le_v.classes_   else 0

    import numpy as np
    X_pred = np.array([[t1_enc, t2_enc, t1_wr, t2_wr, toss_home, field_first, v_enc, season]])
    pred_enc = rf.predict(X_pred)[0]
    proba    = rf.predict_proba(X_pred)[0]

    winner     = le_team.inverse_transform([pred_enc])[0]
    confidence = round(float(proba.max()) * 100, 1)
    t1_prob    = round(float(proba[list(rf.classes_).index(t1_enc)] if t1_enc in rf.classes_ else 0.5) * 100, 1)
    t2_prob    = round(float(proba[list(rf.classes_).index(t2_enc)] if t2_enc in rf.classes_ else 0.5) * 100, 1)

    return {
        'winner': winner,
        'confidence': confidence,
        'team1WinRate': round(t1_wr * 100, 1),
        'team2WinRate': round(t2_wr * 100, 1),
    }

if __name__ == '__main__':
    params = json.loads(sys.argv[1])
    result = predict(params)
    print(json.dumps(result))
