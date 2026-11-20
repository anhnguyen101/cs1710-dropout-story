import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, textwrap
from matplotlib.patches import FancyBboxPatch
INK='#0b0b0b'; INK2='#52514e'
fig=plt.figure(figsize=(14,19),facecolor='#f3f1ea'); ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,14); ax.set_ylim(0,19); ax.axis('off')
ax.text(0.4,18.5,'Data Storyboard — "Dropout is predictable by the end of semester 1"',fontsize=19,fontweight='bold',color=INK,va='center')
ax.text(0.4,18.05,'CS1710 Milestone 7 · Anh Nguyen, Karis Ka, Maggie Peng, Amaka Ihejirika · student_dropout_risk_2026 (100,000 students)',fontsize=11.5,color=INK2,va='center')
W=6.5; H=8.5
cols=[('1 · HOOK','#ffe9a8',0.4,9.0),('2 · RISING INSIGHTS','#cfe3fb',7.1,9.0),('3 · MAIN MESSAGE','#ffd0c2',0.4,0.3),('4 · SOLUTION','#cdeedd',7.1,0.3)]
for title,color,x,y in cols:
    ax.add_patch(FancyBboxPatch((x,y),W,H,boxstyle='round,pad=0.02,rounding_size=0.15',fc='#fbfaf6',ec='#d8d5cc',lw=1.2))
    ax.add_patch(FancyBboxPatch((x,y+H-0.75),W,0.75,boxstyle='round,pad=0.02,rounding_size=0.15',fc=color,ec='none'))
    ax.text(x+W/2,y+H-0.37,title,ha='center',va='center',fontsize=14.5,fontweight='bold',color=INK)
def note(x,y,h,head,body,color,viz=None):
    ax.add_patch(FancyBboxPatch((x+0.2,y),W-0.4,h,boxstyle='round,pad=0.02,rounding_size=0.08',fc=color,ec='none'))
    ax.text(x+0.35,y+h-0.25,head,fontsize=12,fontweight='bold',color=INK,va='top')
    ax.text(x+0.35,y+h-0.62,textwrap.fill(body,72),fontsize=10.2,color=INK,va='top',linespacing=1.35)
    if viz: ax.text(x+0.35,y+0.13,textwrap.fill('VIZ: '+viz,72),fontsize=9.3,color=INK2,va='bottom',style='italic')
# Hook (x=0.4, y from 9.0 to 17.5)
x=0.4; c='#fff3c4'
note(x,14.9,2.0,'Hero number: 1 in 3',"32% of the 100,000 students in the dataset drop out. Open on a single oversized number so the scale lands before any chart does.",c,'hero stat tile, animated count-up from 0 to 32,000')
note(x,12.1,2.6,'Two students, same profile',"Meet two students: same major, same age, same gender, same nationality. One graduates, one leaves. Nothing on the 'who you are' card tells them apart. Audience question: what would you need to know to guess which one leaves?",c,'side-by-side profile cards; demographics shown, outcomes hidden until click')
note(x,9.6,2.3,'The question',"Can you tell who will drop out by the end of their first semester? The rest of the story answers yes, and shows which signals to watch.",c,'single-line prompt, then scroll cue into the insights')
# Rising
x=7.1; c='#e3eefc'
note(x,15.3,1.6,"Step 1 · It's not who you are","Dropout is ~32% in every major, gender, nationality, age and study mode. The flat bars are the point.",c,'small multiples of flat bars by demographic (Amaka)')
note(x,13.4,1.7,'Step 2 · Semester-1 grades split the room',"82% of students with year-1 GPA under 1.5 leave vs 2% above 3.5. Each failed unit adds ~10 points of dropout risk (0 units: 4%, 5 units: 56%).",c,'GPA-bin bars + units-failed staircase; semester toggle from Dashboard 1 (Anh)')
note(x,11.4,1.8,'Step 3 · Grades are driven by engagement',"Attendance, submitted assignments, LMS logins and library visits all track GPA; missed deadlines go the other way (dropout 10% at 0 missed vs 44% at 3).",c,'attendance x GPA scatter with brush, missed-deadline bars (Karis)')
note(x,9.1,2.1,'Step 4 · Outside pressures feed the grades',"Low income (43%), first-gen (37%), tuition behind (44%), part-time job (40%, rising with hours) and stress 8+ (39%) each raise risk, mostly by eroding attendance and GPA. Sleep buffers stress (7.1 at <5h vs 5.7 at 8h+).",c,'income x first-gen grouped bars, work-hours bars, stress 1-10 bars (Amaka, Maggie)')
# Main
x=0.4; c='#ffe2d8'
note(x,5.6,2.3,'The risk ladder',"Seven visible warning signs (sem-1 GPA < 2, 3+ missed deadlines, attendance < 70%, part-time job, low income, tuition behind, stress 8+). Dropout climbs from 5% with none to 23% with two, 59% with four and 95% with all seven.",c,'single-hue bar ladder; hovering a bar lists which signs are most common at that rung')
note(x,3.2,2.2,'Academic signs dominate, pressures amplify',"A 4x4 grid: academic signs on one axis, background pressures on the other. Three academic signs alone = 75%; three pressures alone = 30%. Both = 95%.",c,'heatmap grid, click a cell to see those students highlighted in earlier views')
note(x,0.6,2.4,'So-what statement',"Dropout is not fate: by the end of the first semester a handful of visible warning signs separate a 5% risk from a 95% risk, so help can be targeted months before a student actually leaves.",c,'full-width statement slide over the ladder')
# Solution
x=7.1; c='#dcf3e6'
note(x,5.9,2.0,'For students',"The strongest signals are things you control week to week: go to class, submit on time, log in. Ask for help after the first failed unit, not the third: risk triples between 0 and 2 failed units.",c,'checklist card with the three behaviours')
note(x,3.7,2.0,'For institutions',"An early-alert rule from the data: flag anyone with sem-1 GPA < 2, 3+ missed deadlines or attendance < 70%. Pair academic outreach with financial outreach (tuition plans, work-hour caps) for students carrying 2+ background pressures.",c,'annotated version of the ladder showing where the flag fires')
note(x,1.95,1.65,'Mental-health support reaches the stressed',"Support use climbs from 10% at stress 1 to 50% at stress 10 but is flat across gender, income and major. The gap is the un-flagged high-stress student.",c,'stress x support line (Maggie)')
note(x,0.5,1.3,'Closing interactive',"'Check your own warning signs': toggle the seven signs and watch the dropout rate update. Ends on the hero number, now explained.",c,'toggle panel bound to the ladder')
fig.savefig('figures/milestone7/storyboard.png',dpi=120,facecolor=fig.get_facecolor()); print('ok')
