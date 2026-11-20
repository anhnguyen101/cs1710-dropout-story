import pandas as pd, numpy as np
pd.set_option('display.width',200)
df=pd.read_csv('data/student_dropout_risk_2026.csv')
df['gpa_year1']=(df.gpa_semester_1+df.gpa_semester_2)/2
df['gpa_delta']=df.gpa_semester_2-df.gpa_semester_1
df['fail_rate']=df.units_failed/df.units_enrolled
df['time_commit']=df.weekly_work_hours+df.commute_time_mins/60*5
N=len(df); print('N',N,'dropout rate',df.dropout.mean().round(4), 'NA', df.isna().sum().sum())
def dr(col,bins=None,labels=None):
    s=pd.cut(df[col],bins,labels=labels) if bins is not None else df[col]
    t=df.groupby(s,observed=True).dropout.agg(['mean','size']); t['mean']=(t['mean']*100).round(1); print(t.to_string()); print()
num=df.select_dtypes('number').drop(columns=['person_id'])
print('\n=== ANH ===')
print('Q1 dropout by year-1 GPA'); dr('gpa_year1',[0,1.5,2,2.5,3,3.5,4.01],['<1.5','1.5-2','2-2.5','2.5-3','3-3.5','3.5-4'])
print('GPA by dropout'); print(df.groupby('dropout')[['gpa_semester_1','gpa_semester_2','gpa_year1','gpa_delta']].mean().round(3))
print('sem1 only'); dr('gpa_semester_1',[0,1.5,2,2.5,3,3.5,4.01],['<1.5','1.5-2','2-2.5','2.5-3','3-3.5','3.5-4'])
print('Q2 by units_failed'); dr('units_failed')
print('by fail_rate'); dr('fail_rate',[-0.01,0,0.2,0.4,1.01],['0','0-20%','20-40%','40%+'])
print('Q3 correlations'); 
for t in ['units_failed','fail_rate','gpa_year1','dropout']:
    print(' ',t, num.corr()[t].drop(t).abs().sort_values(ascending=False).head(10).round(3).to_dict())
    print('  signed:', num.corr()[t].drop(t).sort_values().round(3).head(5).to_dict(), num.corr()[t].drop(t).sort_values().round(3).tail(5).to_dict())
print('\n=== AMAKA ===')
print('Q1 first gen'); dr('first_generation')
print(df.groupby(['family_income_level','first_generation']).dropout.agg(['mean','size']).round(3))
print('Q2 income'); print(df.groupby('family_income_level')[['dropout','tuition_up_to_date','part_time_job','weekly_work_hours','attendance_rate','missed_deadlines','gpa_semester_1','units_failed','stress_level','scholarship_holder','sleep_hours','commute_time_mins']].mean().round(3).loc[['Low','Middle','High']])
print('tuition'); dr('tuition_up_to_date'); print('scholarship'); dr('scholarship_holder')
print(df.groupby(['family_income_level','tuition_up_to_date']).dropout.agg(['mean','size']).round(3))
print('Q3 part-time'); dr('part_time_job')
pt=df[df.part_time_job==1]; print('pt n',len(pt),'hrs range',pt.weekly_work_hours.min(),pt.weekly_work_hours.max())
t=pt.groupby(pd.cut(pt.weekly_work_hours,[0,10,15,20,25,30,100],labels=['1-10','11-15','16-20','21-25','26-30','30+'])).dropout.agg(['mean','size']); t['mean']=(t['mean']*100).round(1); print(t)
print('mean hrs by dropout among pt', pt.groupby('dropout').weekly_work_hours.mean().round(2).to_dict())
print(pt.groupby('dropout')[['stress_level','gpa_year1','attendance_rate','sleep_hours']].mean().round(2))
print('\n=== KARIS ===')
print('Q1 corr attendance w gpa1/gpa2/yr', [round(df.attendance_rate.corr(df[c]),3) for c in ['gpa_semester_1','gpa_semester_2','gpa_year1']])
print(df.groupby(pd.cut(df.attendance_rate,[0,60,70,80,90,100.1],labels=['<60','60-70','70-80','80-90','90-100']))[['gpa_year1','dropout','units_failed','assignments_submitted_rate']].mean().round(3))
print('corr assignments w gpa', round(df.assignments_submitted_rate.corr(df.gpa_year1),3), 'lms', round(df.lms_logins_per_week.corr(df.gpa_year1),3),'library',round(df.library_visits_per_month.corr(df.gpa_year1),3),'missed',round(df.missed_deadlines.corr(df.gpa_year1),3))
print('Q2 extracurricular'); dr('extracurricular_activities'); print(df.groupby('extracurricular_activities')[['gpa_year1','stress_level','satisfaction_score','attendance_rate','weekly_work_hours']].mean().round(3))
print('Q3 free time: corr with time_commit / work / commute')
for t in ['attendance_rate','assignments_submitted_rate','lms_logins_per_week','library_visits_per_month','missed_deadlines','gpa_year1','dropout','extracurricular_activities','sleep_hours','stress_level']:
    print('  ',t, round(df.time_commit.corr(df[t]),3), round(df.weekly_work_hours.corr(df[t]),3), round(df.commute_time_mins.corr(df[t]),3))
print(df.groupby(pd.cut(df.time_commit,[-1,0,10,20,30,200],labels=['0','0-10','10-20','20-30','30+']))[['attendance_rate','missed_deadlines','lms_logins_per_week','gpa_year1','dropout']].mean().round(3))
print('missed deadlines'); dr('missed_deadlines')
print('lms'); dr('lms_logins_per_week',[-1,5,10,15,100],['<5','5-10','10-15','15+'])
print('assignments'); dr('assignments_submitted_rate',[0,60,70,80,90,100.1],['<60','60-70','70-80','80-90','90-100'])
print('\n=== MAGGIE ===')
print('Q1 stress'); dr('stress_level'); print(df.groupby('dropout').stress_level.mean().round(3).to_dict())
print('Q2 who seeks support (share with mental_health_support=1)')
for k in ['stress_level','gender','family_income_level','first_generation','disability_status','international_student','course_type','study_mode','dropout','part_time_job','extracurricular_activities','scholarship_holder']:
    print(' ',k, (df.groupby(k).mental_health_support.mean()*100).round(1).to_dict())
print('support rate overall', df.mental_health_support.mean().round(3))
print(df.groupby('mental_health_support')[['stress_level','satisfaction_score','dropout','sleep_hours','gpa_year1']].mean().round(3))
print('dropout by stress x support'); print((df.pivot_table(index='stress_level',columns='mental_health_support',values='dropout')*100).round(1))
print('Q3 sleep-stress corr', round(df.sleep_hours.corr(df.stress_level),3))
print(df.groupby(pd.cut(df.sleep_hours,[0,5,6,7,8,24],labels=['<5','5-6','6-7','7-8','8+']))[['stress_level','dropout','gpa_year1','satisfaction_score']].mean().round(3))
print(df.groupby('stress_level')[['sleep_hours','satisfaction_score','gpa_year1']].mean().round(3))
print('satisfaction'); dr('satisfaction_score')
print('\n=== OVERALL ===')
print(num.corr()['dropout'].drop('dropout').sort_values().round(3).to_string())
for k in ['course_type','study_mode','semester','gender','age','nationality','international_student','disability_status']:
    print(k, (df.groupby(k).dropout.agg(['mean','size']).assign(mean=lambda x:(x['mean']*100).round(1))).to_dict('index'))
# simple logistic-ish: standardized coefficient via numpy least squares on dropout
X=num.drop(columns=['dropout']).copy(); X=(X-X.mean())/X.std(); X['const']=1
beta,*_=np.linalg.lstsq(X.values, df.dropout.values, rcond=None)
print('LPM std coefs:', pd.Series(beta,index=X.columns).drop('const').sort_values().round(4).to_string())
