# ------------------- Importing modules. ------------------- #
# Own functions.
import myfunctions
# General.
import pandas as pd
import numpy as np
import time
import pickle
# Pipelining.
from sklearn.pipeline import make_pipeline
from sklearn.pipeline import Pipeline
# Vectorizing and preprocessing.
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
# Grid Search.
from sklearn.model_selection import GridSearchCV
# Plotting.
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib import rc
# Classifying.
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
# Evaluating.
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
from sklearn.metrics import confusion_matrix

# ------------------- Defining functions. ------------------- #

def read_split_data(path, tuning_set = False, print_n = True):
    '''
    Read data, modify label, shuffle data and split it into training,
    test and optionally "tuning" sets while keeping all datasets
    equally balanced. Optionally print information about the different sets.
    '''
    # Reading data for training classifier.
    origin_df = pd.read_csv(path)

    # Modifying sentiment values for positive sentiments from 4 to 1.
    origin_df.loc[origin_df.sentiment == 4, "sentiment"] = 1

    # Shuffling data.
    origin_df = origin_df.sample(frac = 1)

    if print_n:
    # Getting overview about balance regarding the target variable (sentiment).
        print("Number of tweets in origin data in total: " +
              str(len(origin_df)))
        print("Number of tweets in origin data with sentiment == 1 (positive): " +
              str(len(origin_df[origin_df.sentiment == 1])))
        print("Number of tweets in origin data with sentiment == 0 (negative): " +
              str(len(origin_df[origin_df.sentiment == 0])))

    # Splitting original data into train (70%) and val data (30%) while keeping data balanced (50:50) relating the sentiments.
    # Both will be finally used to train and val the best identified model with its optimal parameters..
    origin_pos_df = origin_df[origin_df.sentiment == 1]
    origin_neg_df = origin_df[origin_df.sentiment == 0]
    n_train_pos_neg = int(len(origin_pos_df) * 0.7)
    train_df = origin_pos_df.head(n = n_train_pos_neg)
    train_df = train_df.append(origin_neg_df.head(n = n_train_pos_neg))
    if print_n:
        print("\nNumber of tweets in training data in total: " +
              str(len(train_df)))
        print("Number of tweets in training data with sentiment == 1 (positive): " +
              str(len(train_df[train_df.sentiment == 1])))
        print("Number of tweets in training data with sentiment == 0 (negative): " +
              str(len(train_df[train_df.sentiment == 0])))
    test_df = origin_pos_df.tail(len(origin_pos_df) - n_train_pos_neg)
    test_df = test_df.append(origin_neg_df.tail(len(origin_pos_df) - n_train_pos_neg))
    if print_n:
        print("\nNumber of tweets in test data in total: " +
              str(len(test_df)))
        print("Number of tweets in test data with sentiment == 1 (positive): " +
              str(len(test_df[test_df.sentiment == 1])))
        print("Number of tweets in test data with sentiment == 0 (negative): " +
              str(len(test_df[test_df.sentiment == 0])))

    if tuning_set:
        # Subsetting train set while keeping data balanced (50:50) relating the sentiments.
        # Resulting "tuning set" will be used for hyperparameter tuning (time reasons).
        n_tuning_pos_neg = int(len(train_df[train_df.sentiment == 1]) * tuning_set)
        tuning_df = train_df[train_df.sentiment == 1].head(n = n_tuning_pos_neg)
        tuning_df = tuning_df.append(train_df[train_df.sentiment == 0].head(n = n_tuning_pos_neg))
        if print_n:
            print("\nNumber of tweets in tuning data in total: " +
                  str(len(tuning_df)))
            print("Number of tweets in tuning data with sentiment == 1 (positive): " +
                  str(len(tuning_df[tuning_df.sentiment == 1])))
            print("Number of tweets in tuning data with sentiment == 0 (negative): " +
                  str(len(tuning_df[tuning_df.sentiment == 0])))

    # Returning extracted sets.
    if tuning_set:
        return [train_df, test_df, tuning_df]
    else:
        return [train_df, test_df]

def vect_model_tuning(train_set, model, vectorizers, preprocessors, params_dict, file_name, njobs = 1):
    '''
    Perform GridSearch with CV (folds = 3) for given training data, classifier, list of vectorizers,
    list of preprocessors and parameter-dictionary.
    Returning evaluation metrics (accuracy, precision, recall, f1-score) for all models in a dataframe.
    '''
    # Initializing dataframe to store information in.
    results = pd.DataFrame(columns=["params", "mean_val_accuracy", "mean_train_accuracy",
                                    "mean_val_precision", "mean_train_precision", "mean_val_recall",
                                    "mean_train_recall", "mean_val_f1", "mean_train_f1",
                                    "model", "vectorizer", "preprocess"])

    model_name = model.__name__

    for vectorizer in vectorizers:
        vect_name = vectorizer.__name__

        for f_preprocessor in preprocessors:
            if f_preprocessor == None:
                preprocess_name = "None"
            else:
                preprocess_name = f_preprocessor.__name__
            print("\nModel: " + model_name)
            print("Vectorizer: " + vect_name)
            print("Preprocessor: " + preprocess_name)

            # Defining pipeline.
            pipeline = Pipeline([('vect', vectorizer(tokenizer = f_preprocessor)),
                                 ('clf', model())])

            # Defining GridSearch procedure.
            gs_procedure = GridSearchCV(
                pipeline,
                params_dict,
                cv = 3,
                iid = False,
                n_jobs = njobs,
                refit = False,
                return_train_score = True,
                scoring = ["accuracy", "precision", "recall", "f1"])

            # Training and validating classifier for each parameter setting.
            gs_fits = gs_procedure.fit(train_set["text"], train_set["sentiment"])

            # Transforming GridSearch results to dataframe.
            gs_res = pd.DataFrame.from_dict(gs_fits.cv_results_, orient='columns', dtype=None, columns=None)

            # Modifying dataframe.
            ## Specifying columns to keep.
            gs_res = gs_res[["params", "mean_test_accuracy", "mean_train_accuracy", "mean_test_precision",
                             "mean_train_precision", "mean_test_recall", "mean_train_recall",
                             "mean_test_f1", "mean_train_f1"]]

            ## Renaming "test"-columns to "val"-columns (since it is actually the validation error, not test error).
            gs_res = gs_res.rename(columns={"mean_test_accuracy": "mean_val_accuracy",
                                            "mean_test_precision": "mean_val_precision",
                                            "mean_test_recall": "mean_val_recall",
                                            "mean_test_f1": "mean_val_f1"})

            ## Adding model name, vectorizer name and preprocess name.
            gs_res["model"] = model_name
            gs_res["vectorizer"] = vect_name
            gs_res["preprocess"] = preprocess_name

            # Appending dataframe to initialized dataframe.
            results = results.append(gs_res)
            print(results)

            # Saving appended dataframe as csv.
            results.to_csv("vect_model_tuning/" + file_name + ".csv", index = False)

    ## Adding model index and ranks to final dataframe (from 1:n_models). Saving as csv.
    n_models = len(results)
    results["model_idx"] = list(range(1, n_models+1))
    results["rank_val_accuracy"] = results["mean_val_accuracy"].rank(ascending = False)
    results["rank_val_accuracy"] = results["rank_val_accuracy"].astype(int)
    results["rank_val_precision"] = results["mean_val_precision"].rank(ascending = False)
    results["rank_val_precision"] = results["rank_val_precision"].astype(int)
    results["rank_val_recall"] = results["mean_val_recall"].rank(ascending = False)
    results["rank_val_recall"] = results["rank_val_recall"].astype(int)
    results["rank_val_f1"] = results["mean_val_f1"].rank(ascending = False)
    results["rank_val_f1"] = results["rank_val_f1"].astype(int)
    results.to_csv("vect_model_tuning/" + file_name + ".csv", index = False)

def define_metric_settings(metric_name, x_range):
    '''Extract information for given metrics. Used within function "visual_model_comparison()".'''

    if metric_name == "accuracy":
        metric_range = [x - 0.075 for x in x_range]
        val_name = "mean_val_accuracy"
        train_name = "mean_train_accuracy"
        color = "blue"

    elif metric_name == "precision":
        metric_range = [x - 0.025 for x in x_range]
        val_name = "mean_val_precision"
        train_name = "mean_train_precision"
        color = "green"

    elif metric_name == "recall":
        metric_range = [x + 0.025 for x in x_range]
        val_name = "mean_val_recall"
        train_name = "mean_train_recall"
        color = "red"

    elif metric_name == "f1":
        metric_range = [x + 0.075 for x in x_range]
        val_name = "mean_val_f1"
        train_name = "mean_train_f1"
        color = "black"

    return {"metric_range": metric_range, "val_name": val_name, "train_name": train_name, "color": color}

def visual_model_comparison(metric_list, gs_res, directory, plot_name, x_label = "Model index", top_n = "all"):
    '''
    Compare models regarding specified metrics (acccuracy, precision, recall or/and f1) visually.
    If "top_n" is specified as integer, only top-n-models (according to their mean metrics rank) will be investigated.
    '''

    # Defining font.
    rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
    rc('text', usetex=True)

    ## Specifying models to keep for further investigation. Top-n-models will be considered for further investigation.
    if isinstance(top_n, int):
        # Defining rank criteria which are used to calculate mean rank.
        rank_criteria = []
        for metric in metric_list:
            rank_criteria.append("rank_val_" + metric)
        ### Calculating mean rank for each model. Sorting models according their mean rank ascendingly.
        model_mean_ranks = gs_res[rank_criteria].mean(axis=1)
        model_mean_ranks = pd.DataFrame({'model_idx':gs_res["model_idx"], 'mean_rank':model_mean_ranks}).sort_values(by = ["mean_rank"])
        ### Extracting model indices of top-n-models.
        top_n_indices = list(model_mean_ranks["model_idx"])[0:top_n]
        ### Subsetting data frame to only keep top-n-models.
        gs_res = gs_res.loc[gs_res["model_idx"].isin(top_n_indices)]
        ### Adjusting row indices.
        gs_res = gs_res.set_index([pd.Index(range(0, top_n))])

    # Initializing legend elements.
    legend_elements = []

    # Extracting number of models to visually analyze.
    n_models = len(gs_res)
    model_range = list(range(1, n_models+1))

    # Adding metric values as points.
    for metric in metric_list:

        ## Appending legend element.
        legend_elements.append(Line2D([0], [0], marker = 'o', color = "w",
        markerfacecolor = define_metric_settings(metric, model_range)["color"],
        label = metric.capitalize()))
        ## Defining x-values for plot.
        metric_range = define_metric_settings(metric, model_range)["metric_range"]
        ## Defining column names for metric.
        colname_val = define_metric_settings(metric, model_range)["val_name"]
        colname_train = define_metric_settings(metric, model_range)["train_name"]
        ## Defining color for metric.
        col = define_metric_settings(metric, model_range)["color"]
        ## Initializing model to choose from.
        i = 0
        ## Looping over each x-value.
        for x_metric in metric_range:
            ## Extracting and plotting val_metric and train_metric for current model.
            val_metric = gs_res[colname_val][i]
            train_metric = gs_res[colname_train][i]
            plt.plot(x_metric, val_metric, marker = "o", color = col)
            plt.plot(x_metric, train_metric, marker = "o", color = "grey", alpha = 0.5)
            ## Jumping to next model.
            i = i + 1

    # Plotting line between train and validation metric values to highlight differences.

    ## Transforming metrics to be able to use plt.axvline.
    ### plt.axvline uses values ymin and ymax for 0 is bottom of the plot, 1 the top of the plot.
    ### Since plot ylim differs (not from 0 to 1), metric values have to be adjusted for usage of plt.axvline.
    ## Extracting ymin, ymax.
    axes = plt.gca()
    ylim = axes.get_ylim()
    ## Calculating range of ylim.
    ylim_range = ylim[1] - ylim[0]
    for metric in metric_list:
        ## Defining x-values for plot.
        metric_range = define_metric_settings(metric, model_range)["metric_range"]
        ## Defining column names for metric.
        colname_val = define_metric_settings(metric, model_range)["val_name"]
        colname_train = define_metric_settings(metric, model_range)["train_name"]
        ## Initializing model to choose from.
        i = 0
        ## Looping over each x-value.
        for x_metric in metric_range:
            ## Extracting val_metric and train_metric for current model.
            val_metric = gs_res[colname_val][i]
            train_metric = gs_res[colname_train][i]
            ## Plotting lines between val_metric and train_metric for current model.
            if val_metric <= train_metric:
                vline_min = 1 - (ylim[1] - val_metric) / ylim_range
                vline_max = 1 - (ylim[1] - train_metric) / ylim_range
            else:
                vline_min = 1 - (ylim[1] - train_metric) / ylim_range
                vline_max = 1 - (ylim[1] - val_metric) / ylim_range
            plt.axvline(x_metric, ymin = vline_min, ymax = vline_max, color = "grey", alpha = 0.5)
            ## Jumping to next model.
            i = i + 1

    # Finishing legend.
    legend_elements.append(Line2D([0], [0], marker = 'o', color = "w", alpha = 0.5,
    markerfacecolor = "grey", label = "Training score"))
    legend_elements.append(Line2D([0], [0], color = "grey", alpha = 0.5, lw = 2, label = "Difference"))

    # Plotting.
    if len(legend_elements) > 4:
        ncol_legend = 3
        bbox = (0.5, 1.18)
    elif len(legend_elements) <= 4:
        ncol_legend = 4
        bbox = (0.5, 1.12)
    plt.legend(handles = legend_elements, loc = "upper center", ncol = ncol_legend,
    bbox_to_anchor=bbox, fancybox = True, shadow = False)
    plt.xticks(model_range, (gs_res["model_idx"]))
    plt.xlabel(x_label)
    plt.ylabel("Score")
    plt.savefig(directory + "/" + plot_name + ".png", dpi = 500)
    plt.show()

def fit_best_classifiers(model_dict, train_df, test_df):
    '''
    Given a dictionary with all model pipelines to fit, the classifiers will be fit on the whole training set
    and evaluated on both training and test data.
    The '75%-approach' is also applied and evaluated. The resulting metrics are returned as data frames.
    '''

    # Inizializing dataframe to store results in.
    results_classes = pd.DataFrame(columns=["model_idx",
                                            "mean_val_accuracy", "mean_train_accuracy",
                                            "mean_val_precision", "mean_train_precision", "mean_val_recall",
                                            "mean_train_recall", "mean_val_f1", "mean_train_f1"])

    # Inizializing dataframe to store results in.
    results_probs = pd.DataFrame(columns=["model_idx",
                                          "mean_val_accuracy", "mean_train_accuracy",
                                          "mean_val_precision", "mean_train_precision", "mean_val_recall",
                                          "mean_train_recall", "mean_val_f1", "mean_train_f1"])

    for key in model_dict:

        # Printing progress.
        print(key)

        # Extracting model name and model pipeline.
        model_name = model_dict[key][0]
        model_pipeline = model_dict[key][1]

        # Fitting classifier on whole training set.
        classifier = model_pipeline.fit(train_df["text"], train_df["sentiment"])

        # Saving classifier.
        pickle.dump(classifier, open("best_classifiers/best_" + model_name + "_classifier" + ".sav", 'wb'))

        # Evaluating model using predicted classes.
        train_c_predictions = classifier.predict(train_df["text"])
        test_c_predictions = classifier.predict(test_df["text"])
        train_c_accuracy = accuracy_score(train_df["sentiment"], train_c_predictions)
        train_c_precision = precision_score(train_df["sentiment"], train_c_predictions)
        train_c_recall = recall_score(train_df["sentiment"], train_c_predictions)
        train_c_f1_score = f1_score(train_df["sentiment"], train_c_predictions)
        test_c_accuracy = accuracy_score(test_df["sentiment"], test_c_predictions)
        test_c_precision = precision_score(test_df["sentiment"], test_c_predictions)
        test_c_recall = recall_score(test_df["sentiment"], test_c_predictions)
        test_c_f1_score = f1_score(test_df["sentiment"], test_c_predictions)

        # Storing and saving results using predicted classes.
        results_classes = results_classes.append(pd.DataFrame({
            "model_idx": [model_name],
            "mean_val_accuracy": [test_c_accuracy],
            "mean_train_accuracy": [train_c_accuracy],
            "mean_val_precision": [test_c_precision],
            "mean_train_precision": [train_c_precision],
            "mean_val_recall": [test_c_recall],
            "mean_train_recall": [train_c_recall],
            "mean_val_f1": [test_c_f1_score],
            "mean_train_f1": [train_c_f1_score]}), ignore_index = True)
        results_classes.to_csv("best_classifiers/results_classes.csv", index = False)

        # Evaluating model using predicted class probabilities.
        train_p_predictions = classifier.predict_proba(train_df["text"])[:,1]
        train_df_temp = train_df
        train_df_temp.loc[:, 'prob_pos'] = train_p_predictions
        train_df_temp = train_df_temp.loc[(train_df_temp["prob_pos"] >= 0.75) | (train_df_temp["prob_pos"] <= 0.25)]
        train_p_predictions = train_df_temp.loc[:, "prob_pos"]
        train_p_predictions = train_p_predictions.mask(train_p_predictions >= 0.75, 1)
        train_p_predictions = train_p_predictions.mask(train_p_predictions <= 0.25, 0)

        test_p_predictions = classifier.predict_proba(test_df["text"])[:,1]
        test_df_temp = test_df
        test_df_temp.loc[:, 'prob_pos'] = test_p_predictions
        test_df_temp = test_df_temp.loc[(test_df_temp["prob_pos"] >= 0.75) | (test_df_temp["prob_pos"] <= 0.25)]
        test_p_predictions = test_df_temp.loc[:, "prob_pos"]
        test_p_predictions = test_p_predictions.mask(test_p_predictions >= 0.75, 1)
        test_p_predictions = test_p_predictions.mask(test_p_predictions <= 0.25, 0)

        train_p_accuracy = accuracy_score(train_df_temp["sentiment"], train_p_predictions)
        train_p_precision = precision_score(train_df_temp["sentiment"], train_p_predictions)
        train_p_recall = recall_score(train_df_temp["sentiment"], train_p_predictions)
        train_p_f1_score = f1_score(train_df_temp["sentiment"], train_p_predictions)
        test_p_accuracy = accuracy_score(test_df_temp["sentiment"], test_p_predictions)
        test_p_precision = precision_score(test_df_temp["sentiment"], test_p_predictions)
        test_p_recall = recall_score(test_df_temp["sentiment"], test_p_predictions)
        test_p_f1_score = f1_score(test_df_temp["sentiment"], test_p_predictions)

        # Storing evaluation results in initialized dataframe.
        results_probs = results_probs.append(pd.DataFrame({
            "model_idx": [model_name],
            "mean_val_accuracy": [test_p_accuracy],
            "mean_train_accuracy": [train_p_accuracy],
            "mean_val_precision": [test_p_precision],
            "mean_train_precision": [train_p_precision],
            "mean_val_recall": [test_p_recall],
            "mean_train_recall": [train_p_recall],
            "mean_val_f1": [test_p_f1_score],
            "mean_train_f1": [train_p_f1_score]}), ignore_index = True)
        results_probs.to_csv("best_classifiers/results_probs.csv", index = False)

    # Returning filled dataframes as dictionary.
    return {"results_classes": results_classes, "results_probs": results_probs}

def classify_new_tweets(new_tweets_df, classifier):
    '''
    Given a data frame including tweets and a classifier, the sentiment will be predicted.
    Only tweets with a predicted probability of at least 75% will be kept. The classification
    result will be added to the data frame which will be returned.
    '''
    probs_pos = classifier.predict_proba(new_tweets_df["tweet"])[:,1]
    new_tweets_df.loc[:, 'prob_pos'] = probs_pos
    pos = new_tweets_df.loc[new_tweets_df["prob_pos"] >= 0.75]
    neg = new_tweets_df.loc[new_tweets_df["prob_pos"] <= 0.25]
    total = pos.append(neg)
    total.loc[total["prob_pos"] >= 0.75, "classification"] = "pos"
    total.loc[total["prob_pos"] <= 0.25, "classification"] = "neg"

    return total

def plot_tweets_by_year(by_year_df, plot_name):
    '''
    A plot to compare the regions (UK, Africa South) over time is created and saved.
    '''

    ## Defining font.
    rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
    rc('text', usetex=True)

    africa_df = by_year_df.loc[by_year_df["country"] == "Africa_South"]
    uk_df = by_year_df.loc[by_year_df["country"] == "UK"]

    plt.plot(africa_df["year"], africa_df["percentage"], marker = "o", color = "blue", alpha = 0.5)
    plt.plot(uk_df["year"], uk_df["percentage"], marker = "o", color = "black", alpha = 0.5)

    legend_elements = [Line2D([0], [0], marker = "o" , color = "black", alpha = 0.5, lw = 2, label = "UK"),
                       Line2D([0], [0], marker = "o" , color = "blue", alpha = 0.5, lw = 2, label = "Africa")]

    plt.legend(handles = legend_elements, loc = "upper center", ncol = 2,
               bbox_to_anchor=(0.5, 1.12), fancybox = True, shadow = False)
    plt.xlabel("Year")
    plt.ylabel("Percentage of positive tweets")
    plt.xticks([2015, 2016, 2017, 2018, 2019])
    plt.savefig("by_year/" + plot_name + ".png", dpi = 500)
