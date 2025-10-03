import numpy as np
import pandas as pd
import random
import csv
import ast
import os

#print("Current working directory:", os.getcwd())
def expected_number(diff,R):
    if diff==1:
        R_mid=1400
    elif diff==2:
        R_mid=1500
    elif diff==3:
        R_mid=1600
    t=(R_mid-R)/400
    u=6*(1/(1+10**(t)))
    U=round(u)
    return U

def actual_solved(R):
    if R>=1000 and R<=1300:
        return (random.choices([1,2,3,4,5,6],weights=[0.40,0.40,0.06,0.04,0.03,0.02])[0])
    elif R>1300 and R<=1500:
        return (random.choices([1,2,3,4,5,6],weights=[0.04,0.06,0.80,0.05,0.03,0.02])[0])
    elif R>1500 and R<=1800:
        return (random.choices([1,2,3,4,5,6],weights=[0.025,0.05,0.1,0.4,0.4,0.025])[0])
    elif R>1800:
        return (random.choices([1,2,3,4,5,6],weights=[0.01,0.02,0.02,0.05,0.075,0.825])[0])

def rating_formula(R,diff,V,S,U,A):
    if U!=0:
        R= R+(A*diff*V*S)/U
    elif U==0:
        R=R+(A*diff*V*S)/0.5
    return R

def avg_inc_each_contest(rating_for_each,rating_for_prev):
    total=sum(rating_for_each.values())
    total_1=sum(rating_for_prev.values())
    avg=((total/len(rating_for_each)))
    avg_1=((total_1/len(rating_for_prev)))
    avg_increase=(avg-avg_1)
    return avg_increase


def penalty_rating(R,V,ratings_current,ratings_prev):
    penalty=avg_inc_each_contest(ratings_current,ratings_prev)
    R=R-(penalty*V)
    R=max(1000,R)
    return R

def check_contest_missed(contests_arr):
   
    tmp_arr={i:[] for i in range(1,len(contests_arr)+1)}
    for k in range(1,len(contests_arr)+1):
        count=0
        for i in range(0,len(contests_arr[k])):
            if (contests_arr[k][i]-count)>=3:
                for j in range(3,(contests_arr[k][i]-count)+1):
                    tmp_arr[k].append(contests_arr[k][i]-(j-2))
                count=contests_arr[k][i]
            elif (contests_arr[k][i]-count)<=3:
                count=contests_arr[k][i]
            if (count<=10 and i==(len(contests_arr[k])-1)):
                for p in range (count+2,len(rows)+1):
                    tmp_arr[k].append(p)
    

    return tmp_arr

participants_array={}
with open ('Participant_details.csv' , newline='') as csvfile:
    tmp = csv.DictReader(csvfile)
    for row in tmp:
        participant = int(row['Participant Number'])
        tmp_events = ast.literal_eval(row['Events Participated'])
        participants_array[participant] = tmp_events

rows=[]
with open('event_weights.csv',newline="") as csvfile:
    tmp_1=csv.reader(csvfile)
    next(tmp_1)
    for row in tmp_1:
        rows.append(tuple(row))

participant_in_each={}
for tmp in range(1,len(rows)+1):
    participant_in_each[tmp]=[]


for j in range(1,len(participants_array)+1):
   for i in range(1,len(rows)+1):
       if i in participants_array[j]:
           participant_in_each[i].append(j)
        
contests_for_penalties=check_contest_missed(participants_array).copy()

penalty_for_each={}
for tmp in range(1,len(rows)+1):
    penalty_for_each[tmp]=[]


for j in range(1,len(contests_for_penalties)+1):
   for i in range(1,len(rows)+1):
       if i in contests_for_penalties[j]:
           penalty_for_each[i].append(j)

contests_attended={i:0 for i in range(1,len(participants_array)+1)}

Ratings={i:1000 for i in range(1,len(participants_array)+1)}

Ratings_after_each={}
Ratings_after_each[0]={i:1000 for i in range(1,len(participants_array)+1)}

for i in range(1,len(rows)+1):
    for participant in participant_in_each[i]:
        contests_attended[participant]+=1
        if contests_attended[participant]<3:
            changing_factor=30
            Ratings[participant]=round(rating_formula(Ratings[participant],int(rows[i-1][2]),float(rows[i-1][1]),actual_solved(Ratings[participant]),expected_number(int(rows[i-1][2]),Ratings[participant]),changing_factor))
        elif contests_attended[participant]>=3:
            changing_factor=15
            Ratings[participant]=round(rating_formula(Ratings[participant],int(rows[i-1][2]),float(rows[i-1][1]),actual_solved(Ratings[participant]),expected_number(int(rows[i-1][2]),Ratings[participant]),changing_factor))
    Ratings_after_each[i]=Ratings.copy()

for i in range(1,len(rows)+1):
    for participant in penalty_for_each[i]:
        rating_after_penalty=penalty_rating(Ratings[participant],float(rows[i-1][1]),Ratings_after_each[i],Ratings_after_each[i-1])
        Ratings[participant]=rating_after_penalty
    Ratings_after_each[i]=Ratings.copy()

df = pd.DataFrame(list(Ratings_after_each[1].items()), columns=["Participants Number", "Ratings"])
df.to_csv("contest_1.csv", index=False)
df = pd.DataFrame(list(Ratings_after_each[2].items()), columns=["Participants Number", "Ratings"])
df.to_csv("contest_2.csv", index=False)
df = pd.DataFrame(list(Ratings_after_each[3].items()), columns=["Participants Number", "Ratings"])
df.to_csv("contest_3.csv", index=False)
df = pd.DataFrame(list(Ratings_after_each[4].items()), columns=["Participants Number", "Ratings"])
df.to_csv("contest_4.csv", index=False)
df = pd.DataFrame(list(Ratings_after_each[5].items()), columns=["Participants Number", "Ratings"])
df.to_csv("contest_5.csv", index=False)
df = pd.DataFrame(list(Ratings_after_each[6].items()), columns=["Participants Number", "Ratings"])
df.to_csv("contest_6.csv", index=False)
df = pd.DataFrame(list(Ratings_after_each[7].items()), columns=["Participants Number", "Ratings"])
df.to_csv("contest_7.csv", index=False)
df = pd.DataFrame(list(Ratings_after_each[8].items()), columns=["Participants Number", "Ratings"])
df.to_csv("contest_8.csv", index=False)
df = pd.DataFrame(list(Ratings_after_each[9].items()), columns=["Participants Number", "Ratings"])
df.to_csv("contest_9.csv", index=False)
df = pd.DataFrame(list(Ratings_after_each[10].items()), columns=["Participants Number", "Ratings"])
df.to_csv("contests_overall_standings.csv", index=False)

#for tmp in range(1,11):
    #print(Ratings_after_each[tmp])
#print(Ratings_after_each[10])
