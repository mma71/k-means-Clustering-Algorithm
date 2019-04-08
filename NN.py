import numpy as np
import sys


def distance(p1,p2):
    return np.sum((p1-p2)**2)**0.5

def kMeans(k,X):
    centers=[]
    membershipLabels=[]

    centers.append(X[0])
    chosen=[0]
    while len(centers)!=k:
        maxd=0
        maxi=0
        for i in range(len(X)):
            if i in chosen:
                continue
            totaldist=sum([distance(X[i],c) for c in centers])
            if totaldist>maxd:
                maxd=totaldist
                maxi=i
        membershipLabels.append({})
        centers.append(X[maxi])
        chosen.append(maxi)
    print(centers)
        
    membership=[0]*len(X)
    
    clusters={}
    iteration=1
    while True:
        oldmembership=membership[:]
        clusters={}
        #print('Iteration '+str(iteration))
        #Find new memvership
        for i in range(len(X)):
            dists=[distance(X[i],c) for c in centers]
            idx=dists.index(min(dists))
            membership[i]=idx+1
            if idx in clusters.keys():
                clusters[idx].append(X[i])           
            else:
                clusters[idx]=[X[i]]
        #Find new centers
        for x in range(k):
            centers[x]=np.mean(clusters[x],axis=0)
        
        if (membership==oldmembership) or (iteration>999):
            break
        iteration+=1


    return (centers,clusters,membership)


if len(sys.argv)==3:   
    try:
        k=int(sys.argv[1])    
        fn=sys.argv[2]
        X = np.genfromtxt(fn,usecols=[0,1])
        (centers,clusters,membership)=kMeans(k,X)
        with open('output.txt','w') as f:
            for i,line in enumerate(X):
                f.write('{}\t{}\t{}\n'.format(line[0],line[1],membership[i]))
    except:
        print('Usage: {} k input.txt'.format(sys.argv[0]))
        exit(0)
else:
    for i in range(1,5):
        fn='input{}.txt'.format(i)
        k=i
        if k<2:
            k=2
        print('Running {} with k={}'.format(fn,k))
        X = np.genfromtxt(fn,usecols=[0,1])
        (centers,clusters,membership)=kMeans(k,X)
        with open('output{}.txt'.format(i),'w') as f:
            for i,line in enumerate(X):
                f.write('{}\t{}\t{}\n'.format(line[0],line[1],membership[i]))
        for j in range(1,k+1):
            X2=X[np.array(membership)==j]
            plt.scatter(X2[:,0],X2[:,1])
        plt.show()
