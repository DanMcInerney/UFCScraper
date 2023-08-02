import pytest
import pandas as pd
import numpy as np
import csv

@pytest.fixture(scope="module")
def master():
    f = open('C:/Users/danhm/PycharmProjects/UFCScraper/UFCScraper/master.csv', 'r')
    master = pd.read_csv(f)
    return master
@pytest.fixture(scope="module")
def fight(master, 'Brandon Moreno', 'Alexandre Pantoja'):
    fight = master.loc[(master['player1'] == 'Brandon Moreno' & master['player2'] == 'Alexandre Pantoja')]
    return fight
@pytest.fixture(scope="module")
def correct_headers():
    correct_headers = {
    "p1_height": '5\'7"'
    "p1_reach":
    "p1_rd1_Body":
    "p1_rd1_Clinch":
    "p1_rd1_Ctrl":
    "p1_rd1_Distance":
    "p1_rd1_Ground":
    "p1_rd1_Head":
    "p1_rd1_KD":
    "p1_rd1_Leg":
    "p1_rd1_Rev":
    "p1_rd1_Sig_str":
    "p1_rd1_Sub_att":
    "p1_rd1_Total_str":
    "p1_rd2_Body":
    "p1_rd2_Clinch":
    "p1_rd2_Ctrl":
    "p1_rd2_Distance":
    "p1_rd2_Ground":
    "p1_rd2_Head":
    "p1_rd2_KD":
    "p1_rd2_Leg":
    "p1_rd2_Rev":
    "p1_rd2_Sig_str":
    "p1_rd2_Sub_att":
    "p1_rd2_Total_str":
    "p1_rd3_Body":
    "p1_rd3_Clinch":
    "p1_rd3_Ctrl":
    "p1_rd3_Distance":
    "p1_rd3_Ground":
    "p1_rd3_Head":
    "p1_rd3_KD":
    "p1_rd3_Leg":
    "p1_rd3_Rev":
    "p1_rd3_Sig_str":
    "p1_rd3_Sub_att":
    "p1_rd3_Total_str":
    "p1_rd4_Body":
    "p1_rd4_Clinch":
    "p1_rd4_Ctrl":
    "p1_rd4_Distance":
    "p1_rd4_Ground":
    "p1_rd4_Head":
    "p1_rd4_KD":
    "p1_rd4_Leg":
    "p1_rd4_Rev":
    "p1_rd4_Sig_str":
    "p1_rd4_Sub_att":
    "p1_rd4_Total_str":
    "p1_rd5_Body":
    "p1_rd5_Clinch":
    "p1_rd5_Ctrl":
    "p1_rd5_Distance":
    "p1_rd5_Ground":
    "p1_rd5_Head":
    "p1_rd5_KD":
    "p1_rd5_Leg":
    "p1_rd5_Rev":
    "p1_rd5_Sig_str":
    "p1_rd5_Sub_att":
    "p1_rd5_Total_str":
    "p2_rd1_Body":
    "p2_rd1_Clinch":
    "p2_rd1_Ctrl":
    "p2_rd1_Distance":
    "p2_rd1_Ground":
    "p2_rd1_Head":
    "p2_rd1_KD":
    "p2_rd1_Leg":
    "p2_rd1_Rev":
    "p2_rd1_Sig_str":
    "p2_rd1_Sub_att":
    "p2_rd1_Total_str":
    "p2_rd2_Body":
    "p2_rd2_Clinch":
    "p2_rd2_Ctrl":
    "p2_rd2_Distance":
    "p2_rd2_Ground":
    "p2_rd2_Head":
    "p2_rd2_KD":
    "p2_rd2_Leg":
    "p2_rd2_Rev":
    "p2_rd2_Sig_str":
    "p2_rd2_Sub_att":
    "p2_rd2_Total_str":
    "p2_rd3_Body":
    "p2_rd3_Clinch":
    "p2_rd3_Ctrl":
    "p2_rd3_Distance":
    "p2_rd3_Ground":
    "p2_rd3_Head":
    "p2_rd3_KD":
    "p2_rd3_Leg":
    "p2_rd3_Rev":
    "p2_rd3_Sig_str":
    "p2_rd3_Sub_att":
    "p2_rd3_Total_str":
    "p2_rd4_Body":
    "p2_rd4_Clinch":
    "p2_rd4_Ctrl":
    "p2_rd4_Distance":
    "p2_rd4_Ground":
    "p2_rd4_Head":
    "p2_rd4_KD":
    "p2_rd4_Leg":
    "p2_rd4_Rev":
    "p2_rd4_Sig_str":
    "p2_rd4_Sub_att":
    "p2_rd4_Total_str":
    "p2_rd5_Body":
    "p2_rd5_Clinch":
    "p2_rd5_Ctrl":
    "p2_rd5_Distance":
    "p2_rd5_Ground":
    "p2_rd5_Head":
    "p2_rd5_KD":
    "p2_rd5_Leg":
    "p2_rd5_Rev":
    "p2_rd5_Sig_str":
    "p2_rd5_Sub_att":
    "p2_rd5_Total_str":
    "p2_height":
    "p2_reach":
    }

    assert correct_headers in fight.columns

