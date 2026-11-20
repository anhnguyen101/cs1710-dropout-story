import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
BLUE='#2a78d6'; ORANGE='#eb6834'; AQUA='#1baf7a'; VIOLET='#6250d6'; INK='#0b0b0b'; INK2='#52514e'; SURF='#fcfcfb'; GRID='#e6e5e1'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.edgecolor':INK2,'axes.labelcolor':INK2,'xtick.color':INK2,'ytick.color':INK2,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':SURF,'axes.facecolor':SURF,'axes.titlecolor':INK,'axes.titleweight':'bold','axes.titlesize':11})
df=pd.read_csv('data/student_dropout_risk_2026.csv')
df['gpa_year1']=(df.gpa_semester_1+df.gpa_semester_2)/2; df['fail_rate']=df.units_failed/df.units_enrolled; df['time_commit']=df.weekly_work_hours+df.commute_time_mins/60*5
def pct(ax,vals,labels,color=BLUE,title='',xlabel='',ylim=100):
    b=ax.bar(range(len(vals)),vals,color=color,width=0.7)
    for i,v in enumerate(vals): ax.text(i,v+1.5,f'{v:.0f}%',ha='center',va='bottom',fontsize=9.5,color=INK)
    ax.set_xticks(range(len(vals))); ax.set_xticklabels(labels,fontsize=9.5); ax.set_ylim(0,ylim); ax.set_ylabel('Dropout rate (%)'); ax.set_title(title,loc='left'); ax.set_xlabel(xlabel); ax.yaxis.grid(True,color=GRID); ax.set_axisbelow(True)
def save(fig,name,sup):
    fig.suptitle(sup,x=0.01,ha='left',fontsize=13,fontweight='bold',color=INK); fig.tight_layout(rect=[0,0,1,0.96]); fig.savefig(f'figures/milestone7/{name}.png',dpi=150); plt.close(fig)
# ---- Anh
fig,ax=plt.subplots(3,1,figsize=(8.5,12.5))
g=df.groupby(pd.cut(df.gpa_year1,[0,1.5,2,2.5,3,3.5,4.01],labels=['<1.5','1.5–2','2–2.5','2.5–3','3–3.5','3.5–4']),observed=True).dropout.mean()*100
pct(ax[0],g.values,g.index,title='Dropout rate by year-1 GPA',xlabel='Mean GPA, semesters 1–2')
g=df[df.units_failed<=10].groupby('units_failed').dropout.mean()*100
pct(ax[1],g.values,[str(int(i)) for i in g.index],title='Dropout rate by units failed',xlabel='Units failed (0–10 shown)')
c=df.select_dtypes('number').drop(columns=['person_id','units_failed','units_passed','gpa_year1']).corr()['fail_rate'].drop('fail_rate')
c=c.reindex(c.abs().sort_values(ascending=False).index)[:9][::-1]
names={'gpa_semester_1':'Semester-1 GPA','gpa_semester_2':'Semester-2 GPA','dropout':'Dropout','missed_deadlines':'Missed deadlines','assignments_submitted_rate':'Assignments submitted','library_visits_per_month':'Library visits','attendance_rate':'Attendance rate','lms_logins_per_week':'LMS logins','admission_grade':'Admission grade','weekly_work_hours':'Weekly work hours','stress_level':'Stress level','tuition_up_to_date':'Tuition up to date'}
ax[2].barh([names.get(i,i) for i in c.index],c.values,color=[ORANGE if v>0 else BLUE for v in c.values],height=0.65)
for i,v in enumerate(c.values): ax[2].text(v+(0.02 if v>0 else -0.02),i,f'{v:+.2f}',va='center',ha='left' if v>0 else 'right',fontsize=9.5,color=INK)
ax[2].axvline(0,color=INK2,lw=0.8); ax[2].set_xlim(-1,0.7); ax[2].set_title('What correlates with failing units',loc='left'); ax[2].set_xlabel('Pearson r'); ax[2].tick_params(axis='y',labelsize=8.5)
save(fig,'anh','Anh Nguyen — grades & academic performance (n = 100,000 students)')
# ---- Amaka
fig,ax=plt.subplots(3,1,figsize=(8.5,12.5))
p=df.pivot_table(index='family_income_level',columns='first_generation',values='dropout').loc[['Low','Middle','High']]*100
x=np.arange(3); w=0.36
ax[0].bar(x-w/2,p[0],w,color=BLUE,label='Continuing-generation'); ax[0].bar(x+w/2,p[1],w,color=ORANGE,label='First-generation')
for i in range(3):
    ax[0].text(x[i]-w/2,p[0].iloc[i]+1.5,f'{p[0].iloc[i]:.0f}%',ha='center',fontsize=9.5); ax[0].text(x[i]+w/2,p[1].iloc[i]+1.5,f'{p[1].iloc[i]:.0f}%',ha='center',fontsize=9.5)
ax[0].set_xticks(x); ax[0].set_xticklabels(['Low income','Middle income','High income']); ax[0].set_ylim(0,70); ax[0].set_ylabel('Dropout rate (%)'); ax[0].set_title('Dropout by family income and first-gen status',loc='left'); ax[0].legend(frameon=False,fontsize=9.5); ax[0].yaxis.grid(True,color=GRID); ax[0].set_axisbelow(True)
p=df.pivot_table(index='family_income_level',columns='tuition_up_to_date',values='dropout').loc[['Low','Middle','High']]*100
ax[1].bar(x-w/2,p[1],w,color=BLUE,label='Tuition up to date'); ax[1].bar(x+w/2,p[0],w,color=ORANGE,label='Behind on tuition')
for i in range(3):
    ax[1].text(x[i]-w/2,p[1].iloc[i]+1.5,f'{p[1].iloc[i]:.0f}%',ha='center',fontsize=9.5); ax[1].text(x[i]+w/2,p[0].iloc[i]+1.5,f'{p[0].iloc[i]:.0f}%',ha='center',fontsize=9.5)
ax[1].set_xticks(x); ax[1].set_xticklabels(['Low income','Middle income','High income']); ax[1].set_ylim(0,70); ax[1].set_ylabel('Dropout rate (%)'); ax[1].set_title('Dropout by income and tuition status',loc='left'); ax[1].legend(frameon=False,fontsize=9.5); ax[1].yaxis.grid(True,color=GRID); ax[1].set_axisbelow(True)
pt=df[df.part_time_job==1]
g=pt.groupby(pd.cut(pt.weekly_work_hours,[0,10,15,20,25,30,100],labels=['5–10','11–15','16–20','21–25','26–30','31–40']),observed=True).dropout.mean()*100
pct(ax[2],g.values,g.index,title='Dropout by work hours (part-time workers)',xlabel='Weekly work hours',ylim=70)
ax[2].axhline(df[df.part_time_job==0].dropout.mean()*100,color=INK2,ls='--',lw=1); ax[2].text(-0.45,df[df.part_time_job==0].dropout.mean()*100+1.2,'students with no job: 25%',ha='left',fontsize=9,color=INK2)
save(fig,'amaka','Amaka Ihejirika — demographics, socioeconomic & institutional factors')
# ---- Karis
fig,ax=plt.subplots(3,1,figsize=(8.5,12.5))
bins=pd.cut(df.attendance_rate,[0,60,70,80,90,100.1],labels=['<60','60–70','70–80','80–90','90–100'])
g=df.groupby(bins,observed=True).agg(gpa=('gpa_year1','mean'),dr=('dropout','mean'))
ax[0].bar(range(5),g.gpa,color=BLUE,width=0.7)
for i,v in enumerate(g.gpa): ax[0].text(i,v+0.04,f'{v:.2f}',ha='center',fontsize=9.5)
ax[0].set_xticks(range(5)); ax[0].set_xticklabels(g.index); ax[0].set_ylim(0,3.2); ax[0].set_ylabel('Mean year-1 GPA'); ax[0].set_xlabel('Attendance rate (%)'); ax[0].set_title('GPA rises with attendance (r = 0.25)',loc='left'); ax[0].yaxis.grid(True,color=GRID); ax[0].set_axisbelow(True)
p=df.pivot_table(index='extracurricular_activities',columns='part_time_job',values='dropout')*100
x=np.arange(2)
ax[1].bar(x-w/2,p[0],w,color=BLUE,label='No part-time job'); ax[1].bar(x+w/2,p[1],w,color=ORANGE,label='Part-time job')
for i in range(2):
    ax[1].text(x[i]-w/2,p[0].iloc[i]+1.5,f'{p[0].iloc[i]:.0f}%',ha='center',fontsize=9.5); ax[1].text(x[i]+w/2,p[1].iloc[i]+1.5,f'{p[1].iloc[i]:.0f}%',ha='center',fontsize=9.5)
ax[1].set_xticks(x); ax[1].set_xticklabels(['No extracurriculars','Extracurriculars']); ax[1].set_ylim(0,60); ax[1].set_ylabel('Dropout rate (%)'); ax[1].set_title('Extracurriculars and dropout',loc='left'); ax[1].legend(frameon=False,fontsize=9.5); ax[1].yaxis.grid(True,color=GRID); ax[1].set_axisbelow(True)
tb=pd.cut(df.time_commit,[-1,0,10,20,30,200],labels=['0','0–10','10–20','20–30','30+'])
g=df.groupby(tb,observed=True).agg(att=('attendance_rate','mean'),md=('missed_deadlines','mean'),dr=('dropout','mean'))
ax[2].plot(range(5),g.att,color=BLUE,marker='o',lw=2,label='Attendance rate (%)')
for i,v in enumerate(g.att): ax[2].text(i,v+1,f'{v:.0f}',ha='center',fontsize=9.5,color=INK)
ax[2].set_ylim(60,85); ax[2].set_xticks(range(5)); ax[2].set_xticklabels(g.index); ax[2].set_xlabel('Weekly hours of work + commute'); ax[2].set_ylabel('Mean attendance rate (%)'); ax[2].set_title('Less free time, lower attendance',loc='left'); ax[2].yaxis.grid(True,color=GRID); ax[2].set_axisbelow(True)
for i,v in enumerate(g.md): ax[2].text(i,61.5,f'{v:.1f} missed deadlines',ha='center',fontsize=8.5,color=INK2)
save(fig,'karis','Karis Ka — academic engagement & behaviour')
# ---- Maggie
fig,ax=plt.subplots(3,1,figsize=(8.5,12.5))
g=df.groupby('stress_level').dropout.mean()*100
pct(ax[0],g.values,[str(i) for i in g.index],title='Dropout rate by self-reported stress',xlabel='Stress level (1–10)',ylim=60)
g=df.groupby('stress_level').mental_health_support.mean()*100
ax[1].plot(g.index,g.values,color=BLUE,marker='o',lw=2,label='All students')
for s,v in zip(g.index,g.values): ax[1].text(s,v+2,f'{v:.0f}%',ha='center',fontsize=8)
d=df.groupby('disability_status').mental_health_support.mean()*100
ax[1].set_ylim(0,60); ax[1].set_xticks(range(1,11)); ax[1].set_xlabel('Stress level (1–10)'); ax[1].set_ylabel('Students using mental-health support (%)'); ax[1].set_title('Who seeks support: stress, not demographics',loc='left'); ax[1].yaxis.grid(True,color=GRID); ax[1].set_axisbelow(True)
ax[1].text(1,52,f'Disability: {d[1]:.0f}% vs {d[0]:.0f}%\nGender, income, major, study mode: all 30–34%',fontsize=9,color=INK2,va='top')
sb=pd.cut(df.sleep_hours,[0,5,6,7,8,24],labels=['<5','5–6','6–7','7–8','8+'])
g=df.groupby(sb,observed=True).agg(st=('stress_level','mean'),dr=('dropout','mean'))
ax[2].bar(range(5),g.st,color=BLUE,width=0.7)
for i,v in enumerate(g.st): ax[2].text(i,v+0.08,f'{v:.1f}',ha='center',fontsize=9.5)
ax[2].set_xticks(range(5)); ax[2].set_xticklabels(g.index); ax[2].set_ylim(0,8.5); ax[2].set_xlabel('Sleep hours per night'); ax[2].set_ylabel('Mean stress level (1–10)'); ax[2].set_title('More sleep, less stress (r = −0.19)',loc='left'); ax[2].yaxis.grid(True,color=GRID); ax[2].set_axisbelow(True)
save(fig,'maggie','Maggie Peng — student wellbeing & support')
# ---- Main message: risk ladder + grid
flags=pd.DataFrame({'GPA<2 (sem 1)':df.gpa_semester_1<2,'3+ missed deadlines':df.missed_deadlines>=3,'Attendance <70%':df.attendance_rate<70,'Part-time job':df.part_time_job==1,'Low income':df.family_income_level=='Low','Behind on tuition':df.tuition_up_to_date==0,'Stress 8+':df.stress_level>=8})
n=flags.sum(axis=1); g=df.groupby(n).dropout.mean()*100
fig,ax=plt.subplots(2,1,figsize=(8.5,10))
cols=[matplotlib.colors.to_hex(c) for c in plt.cm.Blues(np.linspace(0.35,0.95,8))]
ax[0].bar(g.index,g.values,color=cols,width=0.7)
for i,v in zip(g.index,g.values): ax[0].text(i,v+1.5,f'{v:.0f}%',ha='center',fontsize=10)
ax[0].set_xlabel('Number of warning signs present (of 7)'); ax[0].set_ylabel('Dropout rate (%)'); ax[0].set_ylim(0,105); ax[0].set_title('Warning signs stack: 5% with none, 95% with all seven',loc='left'); ax[0].yaxis.grid(True,color=GRID); ax[0].set_axisbelow(True)
ax[0].text(0,88,'Signs: semester-1 GPA < 2, 3+ missed deadlines,\nattendance < 70%, part-time job, low income,\nbehind on tuition, stress 8+',fontsize=9,color=INK2,va='top')
acad=flags[['GPA<2 (sem 1)','3+ missed deadlines','Attendance <70%']].sum(axis=1); bg=flags[['Part-time job','Low income','Behind on tuition']].sum(axis=1)
p=df.pivot_table(index=acad,columns=bg,values='dropout')*100
im=ax[1].imshow(p.values,cmap='Blues',vmin=0,vmax=100,aspect='auto')
for i in range(4):
    for j in range(4): ax[1].text(j,i,f'{p.values[i,j]:.0f}%',ha='center',va='center',fontsize=10,color='white' if p.values[i,j]>55 else INK)
ax[1].set_xticks(range(4)); ax[1].set_yticks(range(4)); ax[1].set_xlabel('Background pressures (part-time job, low income, tuition behind)'); ax[1].set_ylabel('Academic warning signs (GPA, deadlines, attendance)'); ax[1].set_title('Academic signs dominate; background pressures amplify them',loc='left'); ax[1].spines[['left','bottom']].set_visible(False)
save(fig,'main_message','Main message — dropout is predictable from first-semester warning signs')
print('figs done')
