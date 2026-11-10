import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10})
fig=plt.figure(figsize=(14,8.2)); fig.patch.set_facecolor("#F4F6FA")
fig.text(0.02,0.955,"Loan Onboarding Performance Dashboard (Power BI layout mock-up)",fontsize=16,weight="bold",color="#1F3A68")
fig.text(0.02,0.925,"Filters: Date range | Channel (Web / Mobile) | Loan product | Decision path        * Illustrative sample values for layout only",fontsize=9.5,color="#595959")
tiles=[("Applications started","4,820"),("Completion rate","68%"),("Approval rate","57%"),("Avg time to decision","2.4 min"),("KYC failure rate","6.1%"),("Manual review rate","14%")]
for i,(l,v) in enumerate(tiles):
    ax=fig.add_axes([0.02+i*0.163,0.78,0.15,0.12]); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0,0),1,1,boxstyle="round,pad=0.02",fc="white",ec="#BFCFE6",transform=ax.transAxes))
    ax.text(0.08,0.62,v,fontsize=20,weight="bold",color="#1F3A68",transform=ax.transAxes); ax.text(0.08,0.2,l,fontsize=10,color="#595959",transform=ax.transAxes)
ax=fig.add_axes([0.05,0.08,0.36,0.62]); st=["Started","Consent given","KYC submitted","KYC passed","Credit pulled","Decision made"]; vals=[4820,4150,3480,3270,3260,3280*0+3230]
cols=["#1F3A68","#2E5A94","#3D6FB0","#5B8AC6","#7FA6D8","#A9C4E8"]
for i,(s,v) in enumerate(zip(st,vals)):
    w=v/4820; ax.barh(len(st)-1-i,w,left=(1-w)/2,color=cols[i],height=0.8); ax.text(0.5,len(st)-1-i,f"{s}  {v:,}",ha="center",va="center",color="white" if i<4 else "#1F3A68",weight="bold",fontsize=9.5)
ax.set_xlim(0,1); ax.axis("off"); ax.set_title("Application funnel",loc="left",weight="bold",color="#1F3A68")
ax=fig.add_axes([0.45,0.40,0.22,0.30]); lbl=["Auto approved","Auto declined","Manual review"]; v=[57,29,14]
ax.pie(v,labels=[f"{a}\n{b}%" for a,b in zip(lbl,v)],colors=["#548235","#C00000","#ED7D31"],startangle=90,wedgeprops={"width":0.42,"edgecolor":"white"},textprops={"fontsize":9})
ax.set_title("Decision outcomes",loc="left",weight="bold",color="#1F3A68")
ax=fig.add_axes([0.80,0.43,0.18,0.25]); r=["Identity\nmismatch","Doc expired","Address\nunverified","Watchlist\nhit"]; c=[46,22,19,13]
ax.barh(r[::-1],c[::-1],color="#2E75B6"); ax.set_title("KYC failure reasons (%)",loc="left",weight="bold",color="#1F3A68")
for s in ("top","right"): ax.spines[s].set_visible(False)
ax=fig.add_axes([0.48,0.08,0.5,0.25]); wk=[f"W{i}" for i in range(1,13)]; ap=[52,54,53,55,56,55,57,58,56,57,59,58]
ax.plot(wk,ap,marker="o",color="#1F3A68",lw=2); ax.axhline(55,ls="--",color="#C00000",lw=1); ax.text(11.2,55.4,"target 55%",color="#C00000",fontsize=8.5,ha="right")
ax.set_ylim(45,65); ax.set_title("Weekly approval rate (%)",loc="left",weight="bold",color="#1F3A68")
for s in ("top","right"): ax.spines[s].set_visible(False)
plt.savefig("../png/dashboard-mockup.png",dpi=140,facecolor=fig.get_facecolor())
