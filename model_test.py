
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error
from sklearn.pipeline import make_pipeline
from category_encoders import OrdinalEncoder
from sklearn.model_selection import train_test_split

data = pd.read_csv('seoul_houses.csv')
df = data.copy()
df = df.drop(columns=['Unnamed: 0','거래일'])
num_feature = ['세대','인구','자동차등록','인구이동(전입지별)',
               '출생아수(명)', '사망자수(명)' ,'혼인건수(건)','이혼건수(건)']
for col in num_feature:
  df[col] = df[col].str.replace(",","").astype(int)
df['평당가'] = df['거래금액'] / df['전용면적']
df['거래횟수'] = [1]*len(df.index)

## 구별K 선정
from sklearn.cluster import KMeans
구별랭킹 = pd.concat([df.groupby('지역코드').mean()[['평당가','거래금액']].sort_values('평당가',ascending=False),                 
                      df.groupby('지역코드').sum()[['거래횟수']]],
                      axis = 1)
kmeans = KMeans(n_clusters=5)
kmeans.fit(구별랭킹)
구별랭킹['구별K'] = kmeans.labels_

## 매핑
gu_mapper = {gu:k for gu,k in zip(구별랭킹.index,구별랭킹.구별K)}
df['구별K'] = df['지역코드'].copy()
df['구별K'] = df['구별K'].replace(gu_mapper)

## 컬럼명 지정 및 drop
dataset = df.drop(columns=['거래횟수','평당가','지번','-\xa0집세'])
dataset.columns = ['지역코드', '법정동', '아파트', '전용면적', '층', '건축년도', '거래금액', '거래년도', '거래월일', '세대',
       '인구', '세대당인구', '자동차등록', '인구이동(전입지별)', '외국인증권투자', '국고채 3년(평균)',
       '국고채 5년(평균)', '국고채 10년(평균)', '회사채 3년(평균)', 'CD 91물(평균)', '콜금리(1일물,평균)',
       '소비자물가', '- 농축수산물', '- 공업제품', '- 공공서비스', '- 개인서비스', '근원물가', '출생아수(명)',
       '사망자수(명)', '혼인건수(건)', '이혼건수(건)', 'KS11', 'KQ11', 'DJI', 'IXIC', 'VIX',
       'CSI300', 'SSEC', 'DE30', 'FCHI', 'NG', 'GC', 'HG', 'CL', '구별K']

dataset = dataset.drop(columns=['세대당인구','국고채 3년(평균)','국고채 5년(평균)','- 개인서비스','콜금리(1일물,평균)','CSI300','HG'])

## engine함수
def engine(xxx):
  xxx['KRX'] = xxx.KS11 + xxx.KQ11
  xxx = xxx.drop(columns=['KS11','KQ11'])
  return xxx

## dataset에 적용
DF_1 = engine(dataset.copy())
DF_1.shape

dataset = DF_1

## 2021년 기준으로 분리
target='거래금액'
train = dataset[(dataset.거래월일 != '2021-01') | (dataset.거래월일 != '2021-02')].copy()
test = dataset[(dataset.거래월일 == '2021-01') | (dataset.거래월일 == '2021-02')].copy()
print(train.shape,test.shape)
print(test.거래월일.value_counts())

## 2021년 이전 데이터를 훈련, 검증셋으로 분리
X = train.drop(columns=target)
y = train[target]
X_test = test.drop(columns=target)
y_test = test[target]
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=1)

## 모델은 LGBM으로 선정
# from lightgbm import LGBMRegressor
# pipe = make_pipeline(
#     OrdinalEncoder(), 
#     LGBMRegressor()
# )

# pipe.fit(X_train, y_train)
# print('훈련 R^2: ', pipe.score(X_train, y_train))
# print('검증 R^2: ', pipe.score(X_val, y_val))
# print('TEST R^2: ', pipe.score(X_test, y_test))

# print('\n훈련 MAE: ', mean_absolute_error(pipe.predict(X_train), y_train))
# print('검증 MAE: ', mean_absolute_error(pipe.predict(X_val), y_val))
# print('TEST MAE: ', mean_absolute_error(pipe.predict(X_test), y_test))

## 인코딩
encoder = OrdinalEncoder()
X_train_encoded = encoder.fit_transform(X_train)
X_val_encoded = encoder.transform(X_val)
X_test_encoded = encoder.transform(X_test)

# ## 파라미터 튜닝
# lightGB = LGBMRegressor(learning_rate=0.01, max_depth=15, n_estimators=300000, num_leaves=250,
#                       random_state=1, reg_alpha=1, reg_lambda=1, subsample=0.7)

# eval_set = [(X_train_encoded, y_train),
#             (X_val_encoded,y_val), 
#             (X_test_encoded, y_test)]

# lightGB.fit(X_train_encoded, y_train, 
#           eval_set=eval_set,
#           early_stopping_rounds=1000,
#           eval_metric='mae',
#           verbose=100
#          )

# ## 예측측
# y_train_pred = lightGB.predict(X_train_encoded)
# y_val_pred = lightGB.predict(X_val_encoded)
# y_test_pred = lightGB.predict(X_test_encoded)

# ## 검증 및 테스트
# from sklearn.metrics import r2_score
# print("-"*100)
# print('훈련 R2 : ',r2_score(y_train,y_train_pred))
# print('검증 R2 : ',r2_score(y_val,y_val_pred))
# print('TEST R2 : ',r2_score(y_test,y_test_pred))

# ## 검증 및 테스트
# print('훈련 MAE : ',mean_absolute_error(y_train,y_train_pred))
# print('검증 MAE : ',mean_absolute_error(y_val,y_val_pred))
# print('TEST MAE : ',mean_absolute_error(y_test,y_test_pred))

# ## 컬럼명확인
# print('-'*100)
# print('-'*100)

# import joblib
# # save model
# joblib.dump(lightGB, 'lgb.pkl')

# import joblib
# print(joblib.load('lgb.pkl').predict(X_test_encoded.iloc[[1]]))