import numpy as np

class KNearestNeighbor:

    def __init__(self):
        pass
    def train(self,X,y):
        self.X_train=X
        self.y_train=y

    def predict(self,X,k=1,num_loops=0):   #1
        if num_loops== 0:
            dists=self.compute_distances_no_loops(X)
        elif num_loops==1:
            dists=self.compute_distances_one_loop(X)
        elif num_loops==2:
            dists=self.compute_distances_two_loops(X)
        else:
            raise ValueError('Invalid value %d for num_loops' % num_loops)
        return self.predict_labels(dists,k=k)

    def cumpute_distances_two_loops(self,X):
        num_test=X.shape[0]
        num_train=self.X_train.shape[0]
        dists=np.zeros((num_test,num_train))
        print(X.shape,self.X_train.shape)
        for i in range(num_test):
            for j in range(num_train):
                dists[i,j]=np.sqrt(np.sum((X[i,:]-self.X_train[j,:])**2))
        return dists

    def compute_distances_one_loop(self,X):
        num_test=X.shape[0]
        num_train=self.X_train.shape[0]
        dists=np.zeros((num_test,num_train))
        for i in range(num_test):
            dists[i,:]=np.sqrt(np.sum(np.square(self.X_train-X[i,:]),axis=1))
        return dists

    def compute_distances_no_loops(self,X):
        num_test = X.shape[0]
        num_train = self.X_train.shape[0]
        dists = np.zeros((num_test, num_train))
        test_sum=np.sum(np.square(X),axis=1)
        train_sum=np.sum(np.square(self.X_train),axis=1)
        inner_product=np.dot(X,self.X_train.T)
        dists=np.sqrt(-2*inner_product+test_sum.reshape(-1,1)+train_sum)
        return dists

    def predict_labels(self,dists,k=1):   #2
        num_test=dists.shape[0]
        y_pred=np.zeros(num_test)
        for i in range(num_test):
            closest_y=[]
            y_indicies=np.argsort(dists[i,:],axis=0)  #2.1
            closest_y=self.y_train[y_indicies[: k]]   #2.2
            y_pred[i]=np.argmax(np.bincount(closest_y))  #2.3
        return y_pred