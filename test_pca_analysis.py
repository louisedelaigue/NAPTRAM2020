import pandas as pd, numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt

# import cruise data
so279_df = pd.read_csv('./data/so279_df.csv')

# compute PCA analysis
features = ['SBE45_sal', 'SBE38_water_temp','pH_insitu']

# separating out the features
x = so279_df.loc[:, features].values

# separating out the target
y = so279_df.loc[:,['filename']].values

# standardizing the features
x = StandardScaler().fit_transform(x)

# drop nan inside x
def dropna(arr, *args, **kwarg):
    assert isinstance(arr, np.ndarray)
    dropped=pd.DataFrame(arr).dropna(*args, **kwarg).values
    if arr.ndim==1:
        dropped=dropped.flatten()
    return dropped

x = dropna(x)

# run PCA
pca = PCA(n_components=2)
principalComponents = pca.fit_transform(x)
principalDf = pd.DataFrame(data= principalComponents,
                          columns = ['principal component 1',
                                     'principal component 2'])

finalDf = pd.concat([principalDf, so279_df[['filename']]], axis=1)

# vizualize 2D Projection
fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1) 
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('2 component PCA', fontsize = 20)
targets = ['2020-12-08_204002_SO279_STN1_test']
colors = ['r', 'g', 'b']
for target, color in zip(targets,colors):
    indicesToKeep = finalDf['filename'] == target
    ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
               , finalDf.loc[indicesToKeep, 'principal component 2']
               , c = color
               , s = 50)
ax.legend(targets)
ax.grid()


