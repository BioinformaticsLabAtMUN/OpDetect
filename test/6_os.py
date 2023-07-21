# Pandas and numpy for data manipulation
from functools import reduce
from sklearn.metrics import roc_curve, roc_auc_score
from matplotlib import pyplot
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import accuracy_score
import sklearn
import scipy.stats as st
from scipy import stats
import csv
import configargparse
import pickle
import pandas as pd
import numpy as np
from statistics import mean
np.random.seed(42)

# ignore warnings
import warnings 
# warnings.filterwarnings('ignore')

def get_args():
    '''
    get command line arguments
    '''

    p = configargparse.ArgParser(description='OperonSEQer')
    p.add('-c', '--coverage', required=True,
          help='scaled coverage file from RNA-seq', dest='covfile')
    p.add('-g', '--gff', required=True,
          help='modified gff file for organism (chr archive type start stop . strand . geneName)', dest='gff')
    p.add('-o', '--output_name', required=True, help='output name', dest='out')
    p.add('-th', '--threshold', required=False,
          help='threshold for number of calls to become an operon (default is 3)', dest='thresh')
    p.add('-p', '--preds', required=False,
          help='prediction file', dest='preds')
    p.add('-k', '--pickleit', required=False, action='store_true',
          help='if true, saves the processed data as a pickle file', dest='pickleit')
    p.add('-t', '--path', required=False,
          help='optional folder path where input files are and output files go (if not specified, current directory is used)', dest='path')
    p.add('-d', '--delimiter', required=False,
          help='optional argument with the delimiter [tab, space or comma] of the gff file (if not specified, tab is assumed)', dest='deli')
    run_args = p.parse_args()
    return run_args


def extractCoverage(covfile, gff, outfileName, path=None):
    '''
    extract coverage given a coverage file (from bedtools, for example) and a gff file (outfileName is the name of the output file you specify)
    '''
    with open(covfile, "r") as f:
        reader = csv.reader(f, delimiter="\t")
        # next(reader)
        cov = list(reader)

    # to ask whether genes are in an operon, look at intergenic region versus. If it is less than 200 bp, check whether intergenic expression is within 2 fold of gene on either side
    # load genes

    with open(gff, "r") as f:
        reader = csv.reader(f, delimiter="\t")
        # next(reader)
        rna = list(reader)

    covD = {}
    for a in cov:
        if a[0] in covD:
            covD[a[0]][int(a[1])] = float(a[2])
        else:
            covD[a[0]] = {}
            covD[a[0]][int(a[1])] = float(a[2])

    data = []
    length = []
    # values for gene x, gene y, mean_cov_genex, sd_cov_genex, mean_cov_geney, sd_cov_geney, mean intergene x-y, sd intergene x-y,distance, strand x, strand y
    for a in range(0, len(rna)-1):

        chr_a = rna[a][0]
        chr_b = rna[a+1][0]
        start_a = int(rna[a][3])
        stop_a = int(rna[a][4])
        start_i = int(rna[a][4])+1
        stop_i = int(rna[a+1][3])
        dist_genes = stop_i - start_i
        start_b = int(rna[a+1][3])
        stop_b = int(rna[a+1][4])
        strand_a = rna[a][6]
        strand_b = rna[a+1][6]
        covA = []
        covB = []
        if chr_a != chr_b:
            continue
        else:
            x = start_a
            while x < stop_a:
                try:
                    covA.append(covD[chr_a][x])
                except:
                    covA.append(0)
                x += 1
            z = start_b
            while z < stop_b:
                try:
                    covB.append(covD[chr_b][z])
                except:
                    covB.append(0)
                z += 1
            # get mean of only ends of A and B
            if len(covA) ==0:
                meanA=0
                sdA=0
            elif len(covA) < 100:
                meanA = mean(covA)
                sdA = np.std(covA)
            else:
                meanA = mean(covA[-100:])
                sdA = np.std(covA[-100:])

            if len(covB) ==0:
                meanB=0
                sdB=0
            elif len(covB) < 100:
                meanB = mean(covB)
                sdB = np.std(covB)
            else:
                meanB = mean(covB[-100:])
                sdB = np.std(covB[-100:])

            if int(start_i) >= int(stop_i):
                covMid = []
                newMid = int((int(start_b)+int(stop_a))/2)
                newStart = newMid-25
                newStop = newMid+25
                z = newStart
                while z < newStop:
                    try:
                        covMid.append(covD[chr_a][z])
                    except:
                        covMid.append(0)
                    z += 1
                meanMid = mean(covMid)
                sdMid = np.std(covMid)
            else:
                covMid = []
                y = start_i
                while y < stop_i:
                    try:
                        covMid.append(covD[chr_a][y])
                    except:
                        covMid.append(0)
                    y += 1
                meanMid = mean(covMid)
                sdMid = np.std(covMid)
                if len(covMid) > 50:
                    mid = int(len(covMid)/2)
                    startMid = mid-25
                    stopMid = mid+25
                    meanMid = mean(covMid[startMid:stopMid])
                    sdMid = np.std(covMid[startMid:stopMid])
                    meanAend = mean(covMid[0:25])
                    sdAend = np.std(covMid[0:25])
                    meanBend = mean(covMid[-25:])
                    sdBend = np.std(covMid[-25:])
            # Kruskal-wallis test
            try:
                test = stats.kruskal(covA, covB, covMid)
            except ValueError:
                test = 'not valid'
            try:
                testAI = stats.kruskal(covA, covMid)
            except ValueError:
                testAI = 'not valid'
            try:
                testBI = stats.kruskal(covB, covMid)
            except ValueError:
                testBI = 'not valid'
            try:
                testAB = stats.kruskal(covB, covA)
            except ValueError:
                testAB = 'not valid'
            if test != 'not valid' and testAI != 'not valid' and testBI != 'not valid' and testAB != 'not valid':
                data.append([rna[a][8], rna[a+1][8], meanA, sdA, meanB, sdB, meanMid, sdMid, dist_genes, strand_a, strand_b, len(
                    covA), len(covB), len(covMid), test[0], test[1], testAI[0], testAI[1], testBI[0], testBI[1], testAB[0], testAB[1]])

    if path != None:
        outfile = str(path)+str(outfileName)+'_Data_CoverageExtracted.txt'
    else:
        outfile = str(outfileName)+'_Data_CoverageExtracted.txt'
    # print(outfile)
    header = ['']
    with open(outfile, 'w') as writeFile:
        writer = csv.writer(writeFile, delimiter='\t')
        writer.writerows(header)
        writer.writerows(data)

# 2) merge predicitons


def mergePreds(input, pred, outfileName, path=None):
    '''
    with a prediction file in the format Gene1\tGene2\tPrediction, merge with output of coverage extraction (outfileName is the name of the output file you specify)
    '''
    with open(input, "r") as f:
        reader = csv.reader(f, delimiter="\t")
        header1 = next(reader)
        data = list(reader)

    with open(pred, "r") as g:
        reader2 = csv.reader(g, delimiter="\t")
        header2 = next(reader2)
        data2 = list(reader2)

    df = pd.DataFrame(data, columns=['SysName1', 'SysName2', 'meanCov1', 'sdCov1', 'meanCov2', 'sdCov2', 'meanInt', 'sdInt', 'Distance',
                      'Strand1', 'Strand2', 'Length1', 'Length2', 'LengthInt', 'KWs', 'KWp', 'KWAIs', 'KWAIp', 'KWBIs', 'KWBIp', 'KWABs', 'KWABp'])
    df.loc[(df['Strand1'] == df['Strand2']), 'strandMatch'] = 1
    df['strandMatch'] = df['strandMatch'].fillna(0)
    df2 = pd.DataFrame(data2, columns=['SysName1', 'SysName2', 'pred'])

    merged_inner = pd.merge(df, df2, how='left', left_on=[
                            'SysName1', 'SysName2'], right_on=['SysName1', 'SysName2'])
    if path != None:
        outfile = str(path)+str(outfileName)+'_Data_predsMerged.txt'
        merged_inner.to_csv(outfile, sep='\t')
    else:
        merged_inner.to_csv(str(outfileName)+'_Data_predsMerged.txt', sep='\t')

# 3) format data


def formatData(input, outfileName, pred, pickleit=True, path=None):
    '''
    format the data by log transforming p values and dropping NA
    '''
    if pred == False:
        df = pd.read_csv(input, delimiter='\t', names=['SysName1', 'SysName2', 'meanCov1', 'sdCov1', 'meanCov2', 'sdCov2', 'meanInt', 'sdInt',
                         'Distance', 'Strand1', 'Strand2', 'Length1', 'Length2', 'LengthInt', 'KWs', 'KWp', 'KWAIs', 'KWAIp', 'KWBIs', 'KWBIp', 'KWABs', 'KWABp'])
        df.loc[(df['Strand1'] == df['Strand2']), 'strandMatch'] = 1
        df['strandMatch'] = df['strandMatch'].fillna(0)
    else:
        df = pd.read_csv(input, delimiter='\t')

    df['KWp'] += 1e-300
    df['KWAIp'] += 1e-300
    df['KWBIp'] += 1e-300
    df['KWABp'] += 1e-300

    df['log_KWp'] = np.log(df['KWp'])
    df['log_KWAIp'] = np.log(df['KWAIp'])
    df['log_KWBIp'] = np.log(df['KWBIp'])
    df['log_KWABp'] = np.log(df['KWABp'])

    df3 = df.dropna(subset=['Length1'])
    df = df3
    indexNames = df[df['KWs'] == 0].index
    # Delete these row indexes from dataFrame
    df.drop(indexNames, inplace=True)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    if pred == True:
        df['pred'] = df['pred'].fillna(0)
    if path != None:
        filename = str(path)+str(outfileName)+'_Data_Formatted.p'
        outfile = str(path)+str(outfileName)+'_Data_Formatted.txt'
    else:
        filename = str(outfileName)+'_Data_Formatted.p'
        outfile = str(outfileName)+'_Data_Formatted.txt'
    if pickleit == True:
        pickle.dump(df, open(filename, "wb"))
    df.to_csv(outfile, sep='\t')


# 4) Run main script

def CI(a):
    '''
    confidence interval function
    '''
    return st.t.interval(0.95, len(a)-1, loc=np.mean(a), scale=st.sem(a))


def OperonSEQer(input, outfileName, pred, path=None):
    '''
    run the data through ML models 
    '''
    # put together data frames
    dfa2 = pd.read_csv(input, delimiter='\t')  # Select only relevant variables
    dfb = dfa2.dropna(subset=['Length1'])
    dfa2 = dfb
    if pred == True:
        try:
            dfa = dfa2[['Length1', 'Length2', 'LengthInt', 'KWs', 'KWp', 'KWAIs',
                        'KWAIp', 'KWBIs', 'KWBIp', 'KWABs', 'KWABp', 'strandMatch', 'pred']]
        except:
            print(
                "Check the columns of the input file, make sure the following are in the file: ['Length1','Length2','LengthInt','KWs','KWp','KWAIs','KWAIp','KWBIs','KWBIp','KWABs','KWABp','strandMatch','pred']")
            print("Use FormatData.py to get the correct file format")
    else:
        try:
            dfa = dfa2[['Length1', 'Length2', 'LengthInt', 'KWs', 'KWp', 'KWAIs',
                        'KWAIp', 'KWBIs', 'KWBIp', 'KWABs', 'KWABp', 'strandMatch']]
        except:
            print(
                "Check the columns of the input file, make sure the following are in the file: ['Length1','Length2','LengthInt','KWs','KWp','KWAIs','KWAIp','KWBIs','KWBIp','KWABs','KWABp','strandMatch']")
            print("Use FormatData.py to get the correct file format")

    # numeric_cols = [col for col in dfa if dfa[col].dtype.kind != 'O']
    # numeric_cols

    dfa[['KWp']] += 1e-300
    dfa[['KWAIp']] += 1e-300
    dfa[['KWBIp']] += 1e-300
    dfa[['KWABp']] += 1e-300

    dfa[['log_KWp']] = np.log(dfa[['KWp']])
    dfa[['log_KWAIp']] = np.log(dfa[['KWAIp']])
    dfa[['log_KWBIp']] = np.log(dfa[['KWBIp']])
    dfa[['log_KWABp']] = np.log(dfa[['KWABp']])

    if pred == True:
        dfa3 = dfa[['Length1', 'Length2', 'LengthInt', 'KWs', 'log_KWp', 'KWAIs',
                    'log_KWAIp', 'KWBIs', 'log_KWBIp', 'KWABs', 'log_KWABp', 'strandMatch', 'pred']]
    else:
        dfa3 = dfa[['Length1', 'Length2', 'LengthInt', 'KWs', 'log_KWp', 'KWAIs',
                    'log_KWAIp', 'KWBIs', 'log_KWBIp', 'KWABs', 'log_KWABp', 'strandMatch']]

    df = dfa3
    # remove non-same strand
    # Get names of indexes for which column Stock has value No
    indexNames = df[df['KWs'] == 0].index
    # Delete these row indexes from dataFrame
    df.drop(indexNames, inplace=True)
    dfa2.drop(indexNames, inplace=True)
    # df.drop(columns=['strandMatch'], inplace=True)
    # df

    # subset variables
    def format_data(df):
        # Targets are final grade of student
        import sklearn
        labels = df['pred']
        df2 = df.drop(columns=['pred'])
        return df2, labels

    # single species
    if pred == True:
        print('Predictions provided')
        X_test, y_test = format_data(df)
        # print(y_test)
    else:
        X_test = df.copy()
    # multi species
    # X_train, y_train = format_data_2(df)
    # X_test, y_test = format_data_2(testdf)

    # X_train, X_test, y_train, y_test = format_data(df)
    # scale
    X_test2 = X_test.copy()
    X_test2.columns = X_test.columns
    scaler = sklearn.preprocessing.StandardScaler().fit(X_test)
    X_test3 = pd.DataFrame(scaler.transform(X_test))
    X_test3.columns = X_test.columns

    from sklearn.model_selection import cross_validate

    models = ['OS_models/XGB.p', 'OS_models/MLP.p', 'OS_models/SVM.p',
              'OS_models/RF.p', 'OS_models/LR.p', 'OS_models/GNB.p']

    def load_pkl(fname):
        with open(fname, 'rb') as f:
            obj = pickle.load(f)
        return obj

    for model in models:
        model2 = load_pkl(model)
        model_name = str(model).split('.p')[0].split('/')[1]
        if pred == True:
            print('Running '+str(model_name))
            print('testing predicitons by boostrap')
            # configure bootstrap
            n_iterations = 100
            n_size = int(len(y_test) * 0.10)
            stats = []
    # 	    print('this is X_test2')
    # 	    print(X_test2)
            if (model_name == 'XGB') or (model_name == 'RF'):
                tosample = X_test2.copy()
            else:
                tosample = X_test3.copy()
            # print('hi')
            # print(len(tosample['Length1']))
            # print(tosample)
    # 	    print('this is y_test')
    # 	    print(len(y_test))
    # 	    print(type(y_test))
            tosample['pred'] = y_test.tolist()
            # print('here is tosample')
            # print(tosample)
            for i in range(n_iterations):
                # prepare train and test sets
                # print('hello before')
                data = sklearn.utils.resample(tosample, n_samples=n_size)
                # print('here is data')
                # print(data)
                labels = data['pred']
                testset = data.drop(columns=['pred'])
                # print('here is test')
                # print(testset)
                # evaluate model
                # print(model2)
                predictions = model2.predict(testset)
                accuracy = accuracy_score(labels, predictions)
                precision = precision_score(labels, predictions)
                recall = recall_score(labels, predictions)
                f1 = f1_score(labels, predictions)
                tn, fp, fn, tp = confusion_matrix(labels, predictions).ravel()
                specificity = tn / (tn+fp)
                stats.append([accuracy, precision, recall, specificity, f1])
            statsDF = pd.DataFrame(
                stats, columns=['accuracy', 'precision', 'recall', 'specificity', 'f1'])
            cols = statsDF.columns
            # print(model_name)
            # print('statsDF')
            # print(statsDF)
            means = statsDF.mean(axis=0)
            CIs = statsDF[cols].apply(CI)
            # print(CIs.iloc[[0]].values.tolist()[0])
            # for a in CIs:
            #    print(a)
            if (model_name == 'XGB') or (model_name == 'RF'):
                predictions = model2.predict(X_test2)
                lr_probs = model2.predict_proba(X_test2)
            else:
                predictions = model2.predict(X_test3)
                lr_probs = model2.predict_proba(X_test3)
            # keep probabilities for the positive outcome only
            lr_probs = lr_probs[:, 1]
            ns_probs = [0 for _ in range(len(y_test))]
            # calculate scores
            ns_auc = roc_auc_score(y_test, ns_probs)
            lr_auc = roc_auc_score(y_test, lr_probs)
            # summarize scores
            # print('No Skill: ROC AUC=%.3f' % (ns_auc))
            # print('Model: ROC AUC=%.3f' % (lr_auc))
            # calculate roc curves
            ns_fpr, ns_tpr, _ = roc_curve(y_test, ns_probs)
            lr_fpr, lr_tpr, _ = roc_curve(y_test, lr_probs)
            # plot the roc curve for the model
            pyplot.clf()
            fig = pyplot.figure(figsize=(5, 5))
            ax = fig.add_subplot()
            ax.plot(ns_fpr, ns_tpr, linestyle='--', label='No Skill')
            ax.plot(lr_fpr, lr_tpr, marker='.', label='Model')
            ax.title.set_text(str(model_name)+' ROC curve')
            # axis labels
            ax.set(xlabel='False Positive Rate', ylabel='True Positive Rate')
            # show the legend
            ax.legend(bbox_to_anchor=(1, 1), loc="lower right")
            ax.text(0.55, 0.5, 'No Skill: ROC AUC=%.3f' % (ns_auc))
            ax.text(0.55, 0.4, 'Model: ROC AUC=%.3f' % (lr_auc))
            # show the plot
            if path != None:
                fig.savefig(str(path)+str(model_name)+' ROC curve.png')
            else:
                fig.savefig(str(model_name)+' ROC curve.png')
            # Compute ROC curve and ROC area for each class
        else:
            print('Running '+str(model_name)+' - no predictions provided')
            if (model_name == 'XGB') or (model_name == 'RF'):
                predictions = model2.predict(X_test2)
            else:
                predictions = model2.predict(X_test3)

        # print(predictions)
        # tn / (tn + fp)
        # model_name = str(args.model).split('.p')[0].split('/')[-1]
        model_list = [model_name]
        # print(model_list)
        if pred == True:
            results = pd.DataFrame(
                columns=['accuracy', 'precision', 'recall', 'specificity', 'f1'], index=model_list)
            results.loc['means'] = means.tolist()
            # results.loc['lower CI'] = [a_tuple[0] for a_tuple in CIs]
            # results.loc['upper CI'] = [a_tuple[1] for a_tuple in CIs]
            results.loc['lower CI'] = CIs.iloc[[0]].values.tolist()[0]
            results.loc['upper CI'] = CIs.iloc[[1]].values.tolist()[0]
            results.index.name = ''
            results.dropna(inplace=True)
            results.reset_index(inplace=True)
        preds = {}
        preds[model_name] = predictions
        final = pd.DataFrame(columns=['A'])
        final['SysName1'] = dfa2['SysName1']
        final['SysName2'] = dfa2['SysName2']
        # print(len(final['SysName1']))
        # print(len(preds[model_name]))
        final[str(model_name)+'_preds'] = preds[model_name]
        final.drop(columns=['A'], inplace=True)
        if path != None:
            nameRes = str(path)+str(outfileName)+'_' + \
                str(model_name)+'_result.csv'
            namePred = str(path)+str(outfileName)+'_' + \
                str(model_name)+'_predictions.csv'
        else:
            nameRes = str(outfileName)+'_'+str(model_name)+'_result.csv'
            namePred = str(outfileName)+'_'+str(model_name)+'_predictions.csv'
        if pred == True:
            results.to_csv(nameRes, sep='\t', index=False)
        final.to_csv(namePred, sep='\t', index=False)
    print('done with OperonSEQer')
    # exit the script
    exit()
# 5) voting


def voting(files, outfileName, path=None):
    '''
    use result from OperonSEQer to get a voting tally for each operon pair
    '''

    df1 = pd.read_csv(files[0], delimiter='\t')
    df2 = pd.read_csv(files[1], delimiter='\t')
    df3 = pd.read_csv(files[2], delimiter='\t')
    df4 = pd.read_csv(files[3], delimiter='\t')
    df5 = pd.read_csv(files[4], delimiter='\t')
    df6 = pd.read_csv(files[5], delimiter='\t')

    # multiple calls, only use full calls
    df1a = df1.groupby(['SysName1', 'SysName2'])[
        'XGB_preds'].mean().reset_index()
    df2a = df2.groupby(['SysName1', 'SysName2'])[
        'MLP_preds'].mean().reset_index()
    df3a = df3.groupby(['SysName1', 'SysName2'])[
        'SVM_preds'].mean().reset_index()
    df4a = df4.groupby(['SysName1', 'SysName2'])[
        'RF_preds'].mean().reset_index()
    df5a = df5.groupby(['SysName1', 'SysName2'])[
        'LR_preds'].mean().reset_index()
    df6a = df6.groupby(['SysName1', 'SysName2'])[
        'GNB_preds'].mean().reset_index()

    # filter for values that agree (remove anything between 0 and 1)

    df1m = df1a[(df1a['XGB_preds'] == 1) | (df1a['XGB_preds'] == 0)]
    df2m = df2a[(df2a['MLP_preds'] == 1) | (df2a['MLP_preds'] == 0)]
    df3m = df3a[(df3a['SVM_preds'] == 1) | (df3a['SVM_preds'] == 0)]
    df4m = df4a[(df4a['RF_preds'] == 1) | (df4a['RF_preds'] == 0)]
    df5m = df5a[(df5a['LR_preds'] == 1) | (df5a['LR_preds'] == 0)]
    df6m = df6a[(df6a['GNB_preds'] == 1) | (df6a['GNB_preds'] == 0)]

    data_frames = [df1m, df2m, df3m, df4m, df5m, df6m]

    df_merged = reduce(lambda left, right: pd.merge(left, right, on=['SysName1', 'SysName2'],
                                                    how='outer'), data_frames)

    dfm = df_merged.drop_duplicates()
    dfm2 = dfm.dropna()

    col_list = ['XGB_preds',
                'RF_preds', 'LR_preds', 'MLP_preds',
                'GNB_preds', 'SVM_preds']

    dfm2['sum'] = dfm2[col_list].sum(axis=1)

    dfm2['one'] = np.where(dfm2['sum'] >= 1, 1, 0)
    dfm2['two'] = np.where(dfm2['sum'] >= 2, 1, 0)
    dfm2['three'] = np.where(dfm2['sum'] >= 3, 1, 0)
    dfm2['four'] = np.where(dfm2['sum'] >= 4, 1, 0)
    dfm2['five'] = np.where(dfm2['sum'] >= 5, 1, 0)
    dfm2['six'] = np.where(dfm2['sum'] >= 6, 1, 0)

    if path != None:
        dfm2.to_csv(str(path)+str(outfileName) +
                    '_OperonSEQer_vote_result.csv', sep='\t', index=False)
    else:
        dfm2.to_csv(str(outfileName)+'_OperonSEQer_vote_result.csv',
                    sep='\t', index=False)


def OperonMulti(predfile, outname, gff, threshold=3, deli='tab', path=None):
    '''
    thread operons together
    '''

    preds = pd.read_csv(predfile, sep='\t')

    threshdict = {1: 'one', 2: 'two', 3: 'three',
                  4: 'four', 5: 'five', 6: 'six'}
    thresh = threshdict[threshold]
    operons = preds[["SysName1", "SysName2", thresh]]
    operons.columns = ['Gene1', 'Gene2', 'pred']
    if deli == 'tab':
        gff = pd.read_csv(path+gff, sep='\t', header=None)
    elif deli == 'comma':
        gff = pd.read_csv(path+gff, sep=',', header=None)
    elif deli == 'space':
        gff = pd.read_csv(path+gff, sep=' ', header=None)
    genelist = list(gff.iloc[:, 8])
    multioperons = {}
    n = 0
    a = 0
    # print(len(genelist))
    while a < len(genelist)-1:
        inoperon = 1
        templist = [genelist[a]]
        while inoperon == 1:
            subset = operons[operons['Gene1'].str.match(genelist[a])]
            if not subset.empty:
                # if len(subset['pred'])!=1:
                # print('oops two')
                if subset.iloc[0]['pred'] == 0:
                    inoperon = 0
                    a += 1
                    continue
                elif subset.iloc[0]['pred'] != 0:
                    inoperon = 1
                    if subset.iloc[0]['Gene2'] == genelist[a+1]:
                        templist.append(genelist[a+1])
                        a += 1
            else:
                a += 1
                inoperon = 0
        if len(templist) > 1:
            multioperons[n] = templist
        n += 1

    df = pd.DataFrame.from_dict(
        multioperons, orient='index')  # Convert dict to df
    df.to_csv(path+str(outname) + '_OperonSEQer_voteThreshold'+str(threshold) +
              '_operonList.csv', header=False, index=False)  # Convert df to csv


def main():
    args = get_args()
    if args.path:
        extractCoverage(str(args.path)+str(args.covfile),
                        str(args.path)+str(args.gff), str(args.out), str(args.path))
        if args.preds:
            mergePreds(str(args.path)+str(args.out)+'_Data_CoverageExtracted.txt',
                       str(args.path)+str(args.preds), str(args.out), str(args.path))
            formatData(str(args.path)+str(args.out)+'_Data_predsMerged.txt',
                       str(args.out), pred=True, pickleit=True, path=str(args.path))
            OperonSEQer(str(args.path)+str(args.out)+'_Data_Formatted.txt',
                        str(args.out), pred=True, path=str(args.path))
        else:
            formatData(str(args.path)+str(args.out)+'_Data_CoverageExtracted.txt',
                       str(args.out), pred=False, pickleit=True, path=str(args.path))
            OperonSEQer(str(args.path)+str(args.out)+'_Data_Formatted.txt',
                        str(args.out), pred=False, path=str(args.path))
        models = ['XGB', 'MLP', 'SVM', 'RF', 'LR', 'GNB']
        files = []
        for i in models:
            files.append(str(args.path)+str(args.out) +
                         '_'+str(i)+'_predictions.csv')
        voting(files, str(args.out), str(args.path))
        if args.thresh:
            if args.deli:
                OperonMulti(str(args.path)+str(args.out)+'_OperonSEQer_vote_result.csv', str(args.out),
                            str(args.gff), threshold=int(args.thresh), deli=str(args.deli), path=str(args.path))
            else:
                OperonMulti(str(args.path)+str(args.out)+'_OperonSEQer_vote_result.csv', str(
                    args.out), str(args.gff), threshold=int(args.thresh), deli='tab', path=str(args.path))
        else:
            if args.deli:
                OperonMulti(str(args.path)+str(args.out)+'_OperonSEQer_vote_result.csv', str(
                    args.out), str(args.gff), threshold=3, deli=str(args.deli), path=str(args.path))
            else:
                OperonMulti(str(args.path)+str(args.out)+'_OperonSEQer_vote_result.csv', str(
                    args.out), str(args.gff), threshold=3, deli='tab', path=str(args.path))
    else:
        print('No path specified, data files are in the root folder')
        extractCoverage(str(args.covfile), str(args.gff), str(args.out))
        if args.preds:
            mergePreds(str(args.out)+'_Data_CoverageExtracted.txt',
                       str(args.preds), str(args.out))
            formatData(str(args.out)+'_Data_predsMerged.txt',
                       str(args.out), pred=True, pickleit=True)
            OperonSEQer(str(args.out)+'_Data_Formatted.txt',
                        str(args.out), pred=True)
        else:
            formatData(str(args.out)+'_Data_CoverageExtracted.txt',
                       str(args.out), pred=False, pickleit=True)
            OperonSEQer(str(args.out)+'_Data_Formatted.txt',
                        str(args.out), pred=False)
        models = ['XGB', 'MLP', 'SVM', 'RF', 'LR', 'GNB']
        files = []
        for i in models:
            files.append(str(args.out)+'_'+str(i)+'_predictions.csv')
        voting(files, str(args.out))
        if args.thresh:
            if args.deli:
                OperonMulti(str(args.out)+'_OperonSEQer_vote_result.csv', str(args.out),
                            str(args.gff), threshold=int(args.thresh), deli=str(args.deli))
            else:
                OperonMulti(str(args.out)+'_OperonSEQer_vote_result.csv', str(args.out),
                            str(args.gff), threshold=int(args.thresh), deli='tab')
        else:
            if args.deli:
                OperonMulti(str(args.out)+'_OperonSEQer_vote_result.csv',
                            str(args.out), str(args.gff), threshold=3, deli=str(args.deli))
            else:
                OperonMulti(str(args.out)+'_OperonSEQer_vote_result.csv',
                            str(args.out), str(args.gff), threshold=3, deli='tab')
        print('Program complete')


if __name__ == '__main__':
    main()
