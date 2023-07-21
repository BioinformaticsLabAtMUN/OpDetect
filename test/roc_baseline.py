import pandas as pd
import sys
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc


if __name__ == '__main__':

    txid = sys.argv[1]

    # models = ['baseline', 'baseline_train', 'om', 'rh', 'of', 'os']
    # model_names = ['Our Model NE', 'Our Model', 'Operon Mapper', 'Rockhopper', 'Operon Finder', 'OperonSEQer']
    models = ['baseline', 'om', 'rh', 'of', 'os']
    model_names = ['Our Model', 'Operon Mapper', 'Rockhopper', 'Operon Finder', 'OperonSEQer']
    dir = 'outputs'

    # label_path = f'{dir}/model_{txid}.csv'

    # make roc curves for all models in same plot
    plt.figure()
    # put size of figure here
    plt.figure(figsize=(7, 5))
    for i, model in enumerate(models):
        path = f'{dir}/{model}_{txid}.csv'

        # if path does not exist, skip
        try:
            pred = pd.read_csv(path)

            # drop true 2s
            pred = pred[pred.true != 2]
            pred = pred[pred.pred != 2]

            y_true = pred.true
            y_pred = pred.pred
            fpr, tpr, _ = roc_curve(y_true, y_pred)
            roc_auc = auc(fpr, tpr)
            plt.plot(fpr, tpr, label=f'{model_names[i]} (AUC-ROC = {roc_auc:0.2f})')
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






