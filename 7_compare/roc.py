import pandas as pd
import sys
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score, roc_curve, precision_recall_curve, auc


if __name__ == '__main__':

    txid = sys.argv[1]

    #if NE
    if len(sys.argv) > 2 and sys.argv[2] == 'NE':
        models = ['OpDetect', f'OpDetect_{txid}', 'om', 'rh', 'of', 'os']
        model_names = ['OpDetect NE', 'OpDetect', 'Operon Mapper', 'Rockhopper', 'Operon Finder', 'OperonSEQer']
    else:
        models = ['OpDetect', 'om', 'rh', 'of', 'os']
        model_names = ['OpDetect', 'Operon Mapper', 'Rockhopper', 'Operon Finder', 'OperonSEQer']

    dir = 'outputs'

    # make roc curves for all models in same plot
    plt.figure()
    # put size of figure here
    plt.figure(figsize=(7, 5))
    for i, model in enumerate(models):
        path = f'{dir}/{model}_{txid}.csv'

        # RH no prob
        if model == 'rh':
            pred = pd.read_csv(path)
            pred = pred[pred.true != 2]

            y_true = pred.true
            y_prob = pred.pred  #####
            fpr, tpr, _ = roc_curve(y_true, y_prob)
            auroc = roc_auc_score(y_true, y_prob)
            plt.plot(fpr, tpr, label=f'{model_names[i]} (AUROC = {auroc:0.2f})')

        else:
            # if path does not exist, skip
            try:
                pred = pd.read_csv(path)

                # drop true 2s
                pred = pred[pred.true != 2]

                y_true = pred.true
                y_prob = pred.prob
                fpr, tpr, _ = roc_curve(y_true, y_prob)
                auroc = roc_auc_score(y_true, y_prob)
                plt.plot(fpr, tpr, label=f'{model_names[i]} (AUROC = {auroc:0.2f})')

            except:
                print(f'No prediction file for {model} on {txid}.')


    # plot random guess line
    plt.plot([0, 1], [0, 1], color='gray', lw=1.5, linestyle=':', label='Random chance')

    # plot perfect prediction line
    plt.plot([0, 0, 1], [0, 1, 1], color='gray', lw=1.5, linestyle='--', label='Perfect prediction')

    # save plot
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'ROC curve for {txid}')
    plt.legend(loc="lower right", fontsize=10)

    plt.savefig(f'roc/roc_{txid}.png')
    plt.close()








