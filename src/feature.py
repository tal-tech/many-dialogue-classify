import re


class Encoder:
    def __init__(self, keywords_lst_dict, word2int):
        self.word2int = word2int
        self.keywords_lst_dict = keywords_lst_dict

    def keywords_match(self, keyword_str, text):
        # 匹配到多个关键词，无序排列
        #         if "_" not in keyword_str and len(keyword_str) < 3:#过滤掉单个关键词的
        #             return False
        keywords = keyword_str.split("_")
        for word in keywords:
            p = ".*" + word + ".*"
            if not re.findall(p, text):
                return False
        return True

    def cal_class_match_num(self, matched_words):
        matched_words_dict = {}
        for word in matched_words:
            for k, v in self.keywords_lst_dict.items():
                if k not in matched_words_dict:
                    matched_words_dict[k] = []
                if word in v:
                    matched_words_dict[k].append(word)
        return matched_words_dict

    def cal_class_match_rate(self, matched_words_dict):
        match_rates = []
        for k, v in self.keywords_lst_dict.items():
            if k in matched_words_dict:
                molecular, denominator = len(matched_words_dict[k]), len(v)
                match_rates.append(molecular / denominator)
            else:
                match_rates.append(0)

        match_rates.append(0)  # 其他类别
        return match_rates

    def encode_text(self, text):
        features = [0 for _ in range(len(self.word2int))]
        matched_words = []
        for word, idx in self.word2int.items():
            if self.keywords_match(word, text):
                features[idx] = 1
                matched_words.append(word)
        matched_words_dict = self.cal_class_match_num(matched_words)
        match_rates = self.cal_class_match_rate(matched_words_dict)
        features.extend(match_rates)
        return features

    def encode_text_lst(self, text_lst):
        features_lst = []
        for text in text_lst:
            features = self.encode_text(text)
            features_lst.append(features)
        return features_lst
