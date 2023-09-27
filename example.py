from src.main import classfier


in_json = {"in_data": {"dialogue":"家长: 科学课有试课吗\n客服: 您问的是否是以下问题，点击或回复序号即可得到对应问题的答案：<br/>1.了解在线课<br/>\n家长: 科学课有试课吗\n客服: 我帮您看下呢\n家长: 好\n客服: 您好家长\n客服: 我这边帮您看了下目前暂时没有开设科学的单次试听科哦\n客服: 您可以等寒假的时候进行下试听， 寒假的第一节课可以作为试听课   在第二节课开课前申请退费的话会退回全部的课程费用哦\n客服: 您客气啦~\n客服: 山雨欲来风满楼，遇到问题别发愁，欢迎进入人工咨询！很高兴为您服务~\n客服: 您好\n客服: 请您稍等一下，我需要一些时间帮您查询一下，您放心问题已经锁定，马上回来~~\n家长: 好的，谢谢\n客服: 请问还有什么可以帮您的呢~\n客服: 家长如果没有问题的话，请您对我的服务做出评价，五星好评是我们追求的目标，感谢您ღ( ´･ᴗ･` )比心"}}

input_data = [in_json["in_data"]["dialogue"], "家长: 科学课有试课吗"]

#out_json = classfier.classify(in_json["in_data"]["dialogue"])
def many_dialogue(text):
    out_data = []
    for var in text:
        out_data.append(classfier.classify(var))
    return out_data


print(many_dialogue(input_data))

