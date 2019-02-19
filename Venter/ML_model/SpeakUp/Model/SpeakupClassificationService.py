import numpy as np
import pickle

from .SpeakupImportGraph import ImportGraph
from django.conf import settings


class ClassificationService_speakup:
    def __init__(self):
        with open(settings.BASE_DIR + "/Venter/ML_model/SpeakUp/dataset/speakup/speakup_category_index_dictionary_700_clean.pickle", 'rb') as f:
            self.index_complaint_title_map_r = pickle.load(f)

        self.index_complaint_title_map = {}
        for cat in self.index_complaint_title_map_r.keys():
            self.index_complaint_title_map[(self.index_complaint_title_map_r[cat])] = cat
        self.g0 = ImportGraph.get_instance()

    def get_probs_graph(self, model_id, data):
        if model_id == 0:
            model = self.g0
        data = model.process_query(data)
        return model.run(data)

    def get_top_3_cats_with_prob(self, data):
        # This will return np array of size [batch_size,no_class]
        prob1 = self.get_probs_graph(0, data)
        final_sorted = np.argsort(prob1)[::-1]
        # Returns list of size [batch_size] where each list member is dict with 3 key-value pair
        return [{self.index_complaint_title_map[x]: float(prob1[i, x]) for x in final_sorted[i, :3]} for i in
                range(len(final_sorted))]
