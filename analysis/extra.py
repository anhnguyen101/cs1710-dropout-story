import pandas as pd, numpy as np
df=pd.read_csv('data/student_dropout_risk_2026.csv')
df['gpa_year1']=(df.gpa_semester_1+df.gpa_semester_2)/2
flags={'gpa_s1_below_2':df.gpa_semester_1<2,'missed_3plus':df.missed_deadlines>=3,'attendance_below_70':df.attendance_rate<70,'part_time_job':df.part_time_job==1,'low_income':df.family_income_level=='Low','tuition_behind':df.tuition_up_to_date==0,'stress_8plus':df.stress_level>=8}
for k,v in flags.items(): print(k, 'share',round(v.mean()*100,1),'dropout if flag',round(df.dropout[v].mean()*100,1),'if not',round(df.dropout[~v].mean()*100,1))
F=pd.DataFrame(flags); df['nflags']=F.sum(axis=1)
t=df.groupby('nflags').dropout.agg(['mean','size']); t['mean']=(t['mean']*100).round(1); print(t)
# academic-only flags vs background-only
acad=F[['gpa_s1_below_2','missed_3plus','attendance_below_70']].sum(axis=1); bg=F[['part_time_job','low_income','tuition_behind']].sum(axis=1)
print((df.pivot_table(index=acad,columns=bg,values='dropout')*100).round(1))
# good grades but low income+pt job vs bad grades high income no job
print('high gpa(>=3) low income w/ job:', round(df.dropout[(df.gpa_semester_1>=3)&(df.family_income_level=='Low')&(df.part_time_job==1)].mean()*100,1))
print('low gpa(<2) high income no job:', round(df.dropout[(df.gpa_semester_1<2)&(df.family_income_level=='High')&(df.part_time_job==0)].mean()*100,1))
# share of dropouts who had gpa_s1<2.5
print('share of dropouts with gpa_s1<2.5', round((df.gpa_semester_1[df.dropout==1]<2.5).mean()*100,1), 'with >=1 failed unit', round((df.units_failed[df.dropout==1]>=1).mean()*100,1), 'missed>=1', round((df.missed_deadlines[df.dropout==1]>=1).mean()*100,1))
print('gpa by income', df.groupby('family_income_level')[['gpa_semester_1','attendance_rate','missed_deadlines','weekly_work_hours']].mean().round(2))
print('dropout by GPA bin x income'); print((df.pivot_table(index=pd.cut(df.gpa_semester_1,[0,2,3,4.01],labels=['<2','2-3','3-4']),columns='family_income_level',values='dropout',observed=True)*100).round(1))
print('dropout by GPA bin x part_time'); print((df.pivot_table(index=pd.cut(df.gpa_semester_1,[0,2,3,4.01],labels=['<2','2-3','3-4']),columns='part_time_job',values='dropout',observed=True)*100).round(1))
print('attendance x gpa bin dropout'); print((df.pivot_table(index=pd.cut(df.attendance_rate,[0,70,85,100.1],labels=['<70','70-85','85+']),columns=pd.cut(df.gpa_semester_1,[0,2,3,4.01],labels=['<2','2-3','3-4']),values='dropout',observed=True)*100).round(1))
print('gpa_s1 dist', df.gpa_semester_1.describe().round(2).to_dict())
print('extracurricular x pt job', (df.pivot_table(index='extracurricular_activities',columns='part_time_job',values='dropout')*100).round(1))
