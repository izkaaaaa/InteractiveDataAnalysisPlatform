import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

def analysis_function(df,n_clusters=4):
    #df是包括电影名，评分，评价人数和上映年份的DataFrame
    #n_clusters把电影分成几类，默认是4类
    df_copy=df.copy()
    features=df_copy[['评分', '评分人数', '年份']].copy()
    features['评分人数']=np.log1p(features['评分人数'])

    scaler=StandardScaler()
    scaled=scaler.fit_transform(features)

    model=KMeans(n_clusters=n_clusters, random_state=42)
    df_copy['cluster'] = model.fit_predict(scaled)

    result = {
        'clustered_data': df_copy,  # 含聚类标签
        'cluster_centers': model.cluster_centers_,
        'model': model
    }
    return result









