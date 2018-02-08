# a transfer learning algorithm
# paper： Boosting for Transfer Learning
import copy
import math
import numpy as np
import pickle
import traceback
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier


class TrAdaBoostClassifier(object):
    def __init__(self):
        pass
    
    def _init_weights(self, d_sizen, s_sizem):
        '''init w and p

        Parameters
        ----------
        d_sizen: n in the paper, the size of diff-distribution training data
        s_sizem: m in the paper, the size of same-distribution training data
        '''
        w = np.ones(d_sizen + s_sizem)
        return w

    def _set_p(self, w):
        p = w / sum(w)
        return p
    
    def fit(self, TdX, Tdy, TsX, Tsy, S, sample_weights=None, iteration_rounds=10, base_classifier=RandomForestClassifier, **argw):
        '''train the model

        Parameters
        ----------
        TdX: the X of the labeled diff-distribution training data
        Tdy: the label of the labeled diff-distribution training data
        TsX：the X of the labeled same-distribution training data
        Tsy: the label of the labeled same-distribution training data
        S: the dataset of the unlabeled same-distribution test data
        sample_weights: the init weithts of datasets, the size should be (TdX.shape[0] + TsX.shape[0], )
        iteration_rounds: N value
        base_classifier: base classifier
        argw: the base_classifier parameters, maybe include the parameter of this model
        '''
        classifier = base_classifier(**argw)
        d_sizen = TdX.shape[0]
        s_sizem = TsX.shape[0]
        size_nm = d_sizen + s_sizem
        S_size = S.shape[0]
        N = iteration_rounds
        if not sample_weights:
            sample_weights = self._init_weights(d_sizen, s_sizem)
        sample_weights = sample_weights * 1.0
        X = np.concatenate((TdX, TsX), axis=0)
        y = np.concatenate((Tdy, Tsy), axis=0)
        X_S = np.concatenate((X, S), axis=0)
        weights = []
        ps = []
        epilons = []
        betas = []
        predicts = []
        beta = 1 / (1 + (2 * math.log(d_sizen * 1.0/N)))
        for i in range(N):
            # step 1
            p = self._set_p(sample_weights)
            ps.append(p)
            weights.append(copy.deepcopy(sample_weights))
            # step 2
            classifier.fit(X, y, sample_weight=sample_weights)
            predict_y = np.array(classifier.predict(X_S))
            predicts.append(predict_y)
            # step 3
            errors_predict = abs(predict_y[:size_nm] - y)
            # just use the same-distribution data
            epilon = min(sum(sample_weights[d_sizen:] * errors_predict[d_sizen:]/sum(sample_weights[d_sizen:])), 0.5)
            epilons.append(epilon)
            # step 4
            beta_t = epilon / (1 - epilon)
            betas.append(beta_t)
            # step 5
            sample_weights[:d_sizen] = sample_weights[:d_sizen] * beta_t ** errors_predict[:d_sizen]
            sample_weights[d_sizen:] = sample_weights[d_sizen:] * beta_t ** -errors_predict[d_sizen:]
        # output
        last_half = int(N/2)
        left = sum(predicts[last_half:] * np.log([r + 0.001 for r in betas[last_half:]]).reshape((last_half, 1)))
        right = 0.5 * sum(np.log([r + 0.001 for r in betas[last_half:]]))
        result = (left <= right).astype(np.int32)   # negative, so bte turn to lte
        return result


def main():
    datasets_path = r'D:\data\jdcl\datasets\2017-11-20_2017-12-23.csv'
    model_path = r'D:\model\randomforest_2017-11-20_2017-12-23.p'
    cols = []
    # model = pickle.load(open(model_path))
    label_name = 'label_class'
    df = pd.read_csv(datasets_path)
    for col in df.columns:
        try:
            pd.to_numeric(df[col])
            cols.append(col)
        except BaseException:
            # print(col)
            # traceback.print_exc()
            pass
    date_1 = '2017-12-01'
    date_2 = '2017-12-10'
    date_3 = '2017-12-30'
    TdX = df.loc[df.create_time < date_1, cols].values
    TsX = df.loc[(df.create_time > date_1) & (df.create_time < date_2), cols].values
    S = df.loc[(df.create_time > date_2) & (df.create_time < date_3), cols].values
    label_df = df[[label_name, 'create_time']]
    label_d_df = label_df.loc[label_df.create_time < date_1, label_name].values
    label_s_df = label_df.loc[(label_df.create_time > date_1) & (label_df.create_time < date_2), label_name].values
    classifier = TrAdaBoostClassifier()
    result = classifier.fit(TdX, label_d_df, TsX, label_s_df, S, base_classifier=DecisionTreeClassifier)
    print(TdX.shape[0] + TsX.shape[0])
    np.save('result.npy', result)


if __name__ == '__main__':
    main()
