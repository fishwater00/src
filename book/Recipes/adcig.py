try:    from rsf.cluster import *
except: from rsf.proj    import *

# ------------------------------------------------------------
# lags to slant-stacks
# ------------------------------------------------------------
# input:  z-h-x       OR z-t-x
# output: z-tan(a)-x  OR z-dt/dx-x

def cig2ssk(np,op,dp):
    return '''
    slant adj=y np=%d p0=%g dp=%g verb=y
    ''' % (np,op,dp) 

#def cig2ssk(np,op,dp):
#    return '''
#    radon adj=y np=%d p0=%g dp=%g verb=y niter=10
#    ''' % (np,op,dp) 

# ------------------------------------------------------------
# slant-stacks to angle
# ------------------------------------------------------------
# input: z-tan(a)-x
# output z-a-x
#def xsk2angold(na,oa,da):
#    return '''
#    pp2psang2
#    dip=${SOURCES[1]}
#    vpvs=${SOURCES[2]} |
#    tan2ang na=%d a0=%g da=%g
#    ''' % (na,oa,da)

# input: z-dt/dx-x
# output z-a-x
#def tsk2angold(na,oa,da):
#    return '''
#    pp2pstsic na=%d a0=%g da=%g
#    velocity=${SOURCES[1]}
#    dip=${SOURCES[2]}
#    vpvs=${SOURCES[3]}
#    ''' % (na,oa,da)

# ------------------------------------------------------------
def xsk2ang(na,oa,da):
    return '''
    xlagtoang2d na=%d oa=%g da=%g
    dip=${SOURCES[1]}
    vpvs=${SOURCES[2]}
    ''' % (na,oa,da)
def tsk2ang(na,oa,da):
    return '''
    tlagtoang2d na=%d oa=%g da=%g
    dip=${SOURCES[1]}
    vpvs=${SOURCES[2]}
    vel=${SOURCES[3]}
    ''' % (na,oa,da)

# ------------------------------------------------------------
def ciggrey(custom,par):
    return '''
    grey parallel2=n labelrot=n wantaxis=y title=""
    pclip=100 gainpanel=a
    min1=%g max1=%g label1=%s unit1=%s
    screenratio=1.5
    labelsz=6 labelfat=3 titlesz=12 titlefat=3
    %s
    ''' % (
        par['zmin'],par['zmax'],par['lz'],par['uz'],
        par['labelattr']+' '+custom)

def xgrey(custom,par):
    return ciggrey(' label2="\F10 l\F3 \_x\^" unit2=%(ux)s screenratio=%(xratio)g xll=2 yll=1'%par+' '+custom,par)

def zgrey(custom,par):
    return ciggrey(' label2="\F10 l\F3 \_z\^" unit2=%(uz)s xll=2 yll=1'%par+' '+custom,par)

def tgrey(custom,par):
    return ciggrey(' label2="\F10 t\F3" unit2=%(ut)s screenratio=%(tratio)g xll=2 yll=1'%par+' '+custom,par)

def agrey(custom,par):
    return ciggrey(' label2="\F10 q\F3" unit2="\^o\_" screenratio=%(aratio)g xll=2 yll=1 '%par+' '+custom,par)
# ------------------------------------------------------------


# ------------------------------------------------------------
def eparam(v,nhx,ohx,dhx,nhz,ohz,dhz,nht,oht,dht,par):

#    hxmin=ohx
#    hxmax=ohx+(nhx-1)*dhx
#    hzmin=ohz
#    hzmax=ohz+(nhz-1)*dhz
#    hymin=v*(oht)
#    hymax=v*(oht+(nht-1)*dht)
#    dx=hxmax-hxmin
#    dy=hymax-hymin
#    dz=hzmax-hzmin
#    yxeatio=dx/(dx+dy);
#    yzratio=dz/(dz+dy);
#    par['eratio3']=(dz+dy)/(dx+dy);
#    par['epointz']=yzratio;
#    par['epointx']=yxratio;

    dz = (nhz-1)*dhz
    dx = (nhx-1)*dhx
    dt =((nht-1)*dht)*v

    par['eratio']=(dz+dt)/(dx+dt);
    par['epoint1']=dz/(dz+dt);
    par['epoint2']=dx/(dx+dt);
    
    if(par['eratio']>=1):
        par['eheight']=10
    else:
        par['eheight']=12*par['eratio']

#    byte gainpanel=a pclip=100 %s |

# ------------------------------------------------------------
def hparam(v,nhx,ohx,dhx,nhy,ohy,dhy,nht,oht,dht,par):

    dx = (nhx-1)*dhx
    dy = (nhy-1)*dhy
    dt =((nht-1)*dht)*v

    par['hratio']=(dt+dy)/(dx+dy);
    par['hpoint1']=dt/(dt+dy);
    par['hpoint2']=dx/(dx+dy);
    
    if(par['hratio']>=1):
        par['hheight']=10
    else:
        par['hheight']=14*par['hratio']

# ------------------------------------------------------------
def xparam(nhx,ohx,dhx,nz,oz,dz,par):
    dz = (nz-1)*dz
    dx = (nhx-1)*dhx
    par['xratio']=(dz)/(dx);

def tparam(v,nht,oht,dht,nz,oz,dz,par):
    dz = (nz-1)*dz
    dt =((nht-1)*dht)*v

    par['tratio']=(dz)/(dt);
    
# ------------------------------------------------------------
def sparam(v,nhx,ohx,dhx,nz,oz,dz,nht,oht,dht,par):

#    hxmin=ohx
#    hxmax=ohx+(nhx-1)*dhx
#    hzmin=oz
#    hzmax=oz+(nz-1)*dz
#    hymin=v*(oht)
#    hymax=v*(oht+(nht-1)*dht)
#    dx=hxmax-hxmin
#    dy=hymax-hymin
#    dz=hzmax-hzmin
#    yxratio=dx/(dx+dy);
#    yzratio=dz/(dz+dy);   
#    par['spointz']=yzratio;
#    par['spointx']=yxratio;
#    par['sratio3']=1.0;

    dz = (nz -1)*dz
    dx = (nhx-1)*dhx
    dt =((nht-1)*dht)*v
    
    par['sratio']=(dz+dt)/(dx+dt);
    par['spoint1']=dz/(dz+dt);
    par['spoint2']=dx/(dx+dt);
    
    if(par['sratio']>=1):
        par['sheight']=10
    else:
        par['sheight']=13*par['sratio']

# ------------------------------------------------------------
# lz-lx-tau
def egrey(custom,par):
    return '''
    grey3 title="" labelsz=6 labelfat=3 titlesz=12 titlefat=3
    frame1=%d frame2=%d frame3=%d framelabel=n parallel2=n labelrot=n
    label1="\F10 l\F3 \_z\^" unit1=%s
    label2="\F10 l\F3 \_x\^" unit2=%s
    label3="\F10 t\F3      " unit3=%s
    screenratio=%g screenht=%g
    point1=%g point2=%g
    xll=2 yll=1 
    %s
    ''' % ( par['nhz'], par['nhx'], par['nht'],
            par['uz'],
            par['ux'],
            par['ut'],
            par['eratio'],par['eheight'],
            par['epoint1'],par['epoint2'],
            par['labelattr']+' '+custom )

# ------------------------------------------------------------
# tau-lx-ly
def hgrey(custom,par):
    return '''
    grey3 title="" labelsz=6 labelfat=3 titlesz=12 titlefat=3 parallel2=n
    frame1=%d frame2=%d frame3=%d framelabel=n
    label1="\F10 t\F3      " unit1=%s
    label2="\F10 l\F3 \_x\^" unit2=%s
    label3="\F10 l\F3 \_y\^" unit3=%s
    screenratio=%g screenht=%g
    point1=%g point2=%g
    xll=2 yll=1 
    %s
    ''' % ( par['nht'], par['nhx'], par['nhy'],
            par['ut'],
            par['ux'],
            par['uy'],
            par['hratio'],par['hheight'],
            par['hpoint1'],par['hpoint2'],
            par['labelattr']+' '+custom )

# ------------------------------------------------------------
# z-lx-tau
def sgrey(custom,par):
    return '''
    grey3 title="" labelsz=6 labelfat=3 titlesz=12 titlefat=3
    frame1=%d frame2=%d frame3=%d framelabel=n parallel2=n labelrot=n
    label1="z" unit1=%s
    label2="\F10 l\F3 \_x\^" unit2=%s
    label3="\F10 t\F3      " unit3=%s
    screenratio=%g screenht=%g
    point1=%g point2=%g
    xll=2 yll=1 
    %s
    ''' % ( par['nz']/2, par['nhx'], par['nht'],
            par['uz'],
            par['ux'],
            par['ut'],
            par['sratio'],par['sheight'],
            par['spoint1'],par['spoint2'],
            par['labelattr']+' '+custom )


def lgrey(custom,par):
    return '''
    grey title="" pclip=100
    label2="\F10 l\F3 \_x\^" unit2=%s
    label1="\F10 t\F3      " unit1=%s
    screenratio=%g
    xll=2 yll=1
    %s
    ''' % (par['ux'],
           par['ut'],
	   par['lratio'],
	   par['labelattr']+' '+custom)
