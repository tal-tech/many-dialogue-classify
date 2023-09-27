import os
import pickle
from sklearn.metrics import classification_report

base_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class config:
    valid_16_names = os.path.join(base_folder, "data/16_names.lst")
    model_dict = os.path.join(base_folder, "data/lr_16.model")
    keywords_lst_dict = os.path.join(base_folder, "data/kw_lst.dict")
    word2int = os.path.join(base_folder, "data/word2int.dict")
    in_jsons = os.path.join(base_folder, "data/in_jsons.json")
    y_trues = os.path.join(base_folder, "data/test.label")


def load_file(file_path):
    with open(file_path, "rb") as fr:
        data = pickle.load(fr)
    return data


class Evaluation:
    def __init__(self, valid_16_names):
        self.valid_16_names = valid_16_names

    def get_one_labels(self, y_lsts, label):
        y_outs = []
        for y in y_lsts:
            if label in y:
                y_outs.append(1)
            else:
                y_outs.append(0)
        return y_outs

    def evaluate_one_label(self, y_true_lsts, y_pred_lsts, label):
        y_true, y_pred = self.get_one_labels(y_true_lsts, label), self.get_one_labels(y_pred_lsts, label)
        report = classification_report(y_true, y_pred, output_dict=True)
        return report

    def evaluate(self, y_true_lsts, y_pred_lsts):
        outs = []

        for cls in self.valid_16_names[:-1]:
            report = self.evaluate_one_label(y_true_lsts, y_pred_lsts, cls)
            #             print(report)
            precision, recall, support = report["1"]["precision"], report["1"]["recall"], report["1"]["support"]
            print(cls, precision, recall, support, sep="\t")
            outs.append((cls, precision, recall, support))
        p, r, nums = self.weight_pr(outs)
        print("整体", p, r, nums, sep="\t")
        return outs

    def weight_pr(self, outs):
        nums = 0
        tmp_p = 0
        tmp_r = 0
        for out in outs:
            nums += out[3]
            tmp_p += out[1] * out[3]
            tmp_r += out[2] * out[3]
        return tmp_p / nums, tmp_r / nums, nums
