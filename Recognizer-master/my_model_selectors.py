import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences

#build_training: returns training database. This method collects the features for all the words in the training set
#get_all_sequences:
#get_all_Xlengths:
#get_word_sequences:
#get_word_Xlengths: Provides the sequence to train HMMLibrary. It provides 2 lists: first is a concatenation of all the sequences (X i.e the input part) and second is a list of the sequence lengths

class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''
    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None

class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant
    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)

class SelectorCV(ModelSelector):
    #select best model based on average log Likelihood of cross-validation folds
    
    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection using CV
        best_hmm_model, hmm_model = None, None
        best_score = float('-inf')
        
        
        for num_components in range(self.min_n_components, self.max_n_components + 1):
            cv_model_scores = []
            
            try:
                folds = 2
                if (len(self.sequences) > 1):
                    folds = min(len(self.sequences),3)

                #print('number of folds', folds)
                split_method = KFold(n_splits=folds)
            
                for cv_train_idx, cv_test_idx in split_method.split(self.sequences):
                    X_train, lengths_train = combine_sequences(cv_train_idx, self.sequences)
                    X_test, lengths_test = combine_sequences(cv_test_idx, self.sequences)
                
                    hmm_model = GaussianHMM(n_components=num_components, covariance_type="diag", n_iter=1000,random_state=self.random_state, verbose=False).fit(X_train, lengths_train)
                    score = hmm_model.score(X_test, lengths_test)
                    
                    cv_model_scores.append(score) 
            except:
                if self.verbose:
                    print("model created for {} states throws error".format(num_components))
                
            avg_score = np.mean(cv_model_scores) if len(cv_model_scores) > 0 else float('-inf')
            if (avg_score > best_score):
                best_score, best_hmm_model = avg_score, hmm_model
            
        return best_hmm_model

class SelectorBIC(ModelSelector):
    """ select the model with the lowest Bayesian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    
    p = number of parameters
    N = number of data points
    """

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components
        
        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        best_model = None
        #Lower the BIC value the better the mode
        min_score = float('inf')
        for num_components in range(self.min_n_components, self.max_n_components + 1):
            try:
                model = self.base_model(num_components)
                score = model.score(self.X, self.lengths)
                
                
                num_data = self.X.shape[0]
                num_features = self.X.shape[1]
                #num_params = # of transition probabilities + # of means + # of variances + # of initial probabilities
                #num_params = num_components * (num_components - 1) + num_features * 2 * num_components + num_components -1
                num_params = num_components * num_components + num_features * 2 * num_components - 1
                bic_score = -2 * score + np.log(num_data) * num_params
                
                if bic_score < min_score:
                    min_score, best_model = bic_score, model
            except:
                    if self.verbose:
                        print("model created for {} states throws error".format(num_components))
        
        return best_model
            
class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        best_model = None
        best_score = float('-inf')
        
        rest_words = list(self.words)
        rest_words.remove(self.this_word)
        for num_components in range(self.min_n_components, self.max_n_components + 1):
            all_score = 0.0
            try:
                model = self.base_model(num_components)
                score = model.score(self.X, self.lengths)
                
                for r_word in rest_words:
                     r_X, r_lengths = self.hwords[r_word]
                     r_score = model.score(r_X, r_lengths)
                     all_score += r_score
                
                all_avg_score = all_score / len(rest_words)
                
                dic_score = score - all_avg_score
                
                if dic_score > best_score:
                    best_score, best_model = dic_score, model
                    
            except:
                    if self.verbose:
                        print("model created for {} states throws error".format(num_components))
        
        return best_model