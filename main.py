import pathlib
import json

# file_name = 'data/t20160601_1404913.txt'

replace_dict = {
    '\xa0': ' ',
    '\u3000': ' ',
    '．': '.',
    '、': '.',
}

replace_dict.update(
    {chr(i + ord('Ａ')): chr(ord('A') + i) for i in range(0, 26)})


class DefaultEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, object):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


class Paper:
    def __init__(self, title: list):
        self.title = title
        self.questions = []
        self.answer = []

    def __str__(self):
        return f'{self.title}\n{self.questions}'

    def __repr__(self):
        return self.__str__()

    def get_title(self):
        for i in self.title:
            if i:
                return i


class Question:
    def __init__(self, title, choices):
        self.title = title
        self.choices = choices
        # self.parse = ''

        self.format_()

    def __str__(self):
        return f'{self.title}\n{self.choices}'

    def format_(self):
        self.title = self.__fmt_dot(self.title)

        # t = []
        # choice = ' '.join(self.choices)
        # for i in range(0, 27):
        #     idx = choice.index(chr(ord('A') + i))
        #     if idx == -1 or idx > 3:
        #         break
        #     choice = choice.replace(
        #         chr(ord('A') + i), f'\n{chr(ord("A") + i)}')
        # choice = [i for i in choice.split('\n') if i]
        # pass

    @staticmethod
    def __fmt_alpha(s: str) -> str:
        index = s.find('.')
        if index != -1 and s[:index].strip().isdigit():
            s = s[index + 1:]
        return s.strip()

    @staticmethod
    def __fmt_dot(s: str) -> str:
        index = s.find('.')
        if index != -1 and s[:index].strip().isdigit():
            s = s[index + 1:]
        return s.strip()


def parse(file_name):

    with open(file_name, 'r') as f:
        data = [i.strip() for i in f.readlines() if i]
    for k, v in replace_dict.items():
        for i in range(len(data)):
            data[i] = data[i].replace(k, v)

    i = 0
    while i < len(data) and not data[i].split('.')[0].strip().isdigit():
        i += 1

    j = len(data) - 1
    while j >= len(data) - 100 and not '答案' in data[j]:
        j -= 1
    if j <= len(data) - 100:
        answer = []
    else:
        answer = [x for x in data[j + 1:] if x]

    paper = Paper(data[:i])
    paper.answer = answer

    data = data[i:j]

    while i < len(data):
        while i < len(data) and not data[i].split('.')[0].strip().isdigit():
            i += 1
        j = i + 1
        while j < len(data) and not data[j].split('.')[0].strip().isdigit():
            j += 1

        q = [x for x in data[i:j] if x]
        question = Question(q[0], q[1:] if q[1:]
                            else paper.questions[-1].choices)
        paper.questions.append(question)
        i = j

    with open(pathlib.Path('paper/' + paper.get_title() + '.json'), 'w') as f:
        json.dump(paper, f, cls=DefaultEncoder, ensure_ascii=False, indent=4)


def main():
    for file_name in pathlib.Path('data').glob('*.txt'):
        parse(file_name)


if __name__ == "__main__":
    main()
    pass
