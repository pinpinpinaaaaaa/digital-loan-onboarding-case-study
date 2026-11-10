import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(9,7)); ax.set_xlim(0,10); ax.set_ylim(0,10)
ax.axhline(5,color="#808080",lw=1); ax.axvline(5,color="#808080",lw=1)
for (x,y,t,c) in [(2.5,5.4,"KEEP SATISFIED","#FCE4D6"),(7.5,5.4,"MANAGE CLOSELY","#F8CBAD"),(2.5,0.4,"MONITOR","#EEF3FB"),(7.5,0.4,"KEEP INFORMED","#E2EFDA")]:
    ax.text(x,y,t,ha="center",va="center",fontsize=11,weight="bold",color="#404040",bbox=dict(fc=c,ec="none",pad=4))
S=[("Product Owner",8.8,8.6),("Compliance",8.2,8.0),("Risk / Credit",7.5,8.8),("Lending leadership\n(Sponsor)",6.2,9.1),("IT / Engineering",7.4,6.6),
   ("Operations\n(manual review)",8.4,4.0),("Customer Support",6.6,2.6),("InfoSec",3.5,7.4),("Legal",3.0,6.2),("Marketing",3.0,2.8),("Customers",8.6,1.8)]
for n,x,y in S:
    ax.scatter(x,y,s=180,color="#1F3A68",zorder=3); ax.text(x+0.15,y+0.2,n,fontsize=9.5)
ax.set_xlabel("Interest in the project  →",fontsize=11); ax.set_ylabel("Influence / power  →",fontsize=11)
ax.set_xticks([]); ax.set_yticks([]); ax.set_title("Stakeholder Map (Power / Interest Grid)",fontsize=14,weight="bold",color="#1F3A68")
plt.tight_layout(); plt.savefig("../png/stakeholder-map.png",dpi=150)
