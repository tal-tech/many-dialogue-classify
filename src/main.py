from src.utils import load_file, config
from src.feature import Encoder


class Classfier:
    def __init__(self, ):
        # load data
        self.valid_16_names = load_file(config.valid_16_names)
        self.model_dict = load_file(config.model_dict)
        self.keywords_lst_dict = load_file(config.keywords_lst_dict)
        self.word2int = load_file(config.word2int)
        # init feature encoder
        self.encoder = Encoder(self.keywords_lst_dict, self.word2int)

    def predict(self, X_test):
        y_pred_lst = [[] for _ in range(len(X_test))]
        y_prob_lst = [[] for _ in range(len(X_test))]

        for name in self.valid_16_names:
            model = self.model_dict[name]
            y_probs_lst = model.predict_proba(X_test)
            for i in range(len(y_probs_lst)):
                if y_probs_lst[i][1] >= 0.6:
                    y_pred_lst[i].append(name)
                    y_prob_lst[i].append(y_probs_lst[i][1])
        return y_pred_lst, y_prob_lst

    def classify(self, text):
        # try:
        #     assert type(text) == str
        # except:
        #     print("input_json_error")
        #     return {"out_data": [], "code": -1, "msg": "input_json_error"}
        try:
            x_encoded = self.encoder.encode_text_lst([text])
            pred_lst, prob_lst = self.predict(x_encoded)
            pred, prob = pred_lst[0], prob_lst[0]
            out_data = []
            for i in range(len(pred)):
                json_line = {"type": pred[i], "prob": prob[i]}
                out_data.append(json_line)
        except:
            print("model_predict_failed")
            return {"out_data": [], "code": -2, "msg": "model_predict_failed"}

        return {"data": out_data, "code": 0, "msg": "success"}


classfier = Classfier()
