from requests import Session, get
from requests.cookies import create_cookie
from user_agent import generate_user_agent


class Problemator:
    def __init__(self):
        self.categories = {}
        self.load_session()

    def convert_categories(self, categories_dict, id_counter=0):
        converted_data = {}

        for category in categories_dict:
            category_name = category['Display']
            subcategories = category.get('Subcategories', [])

            if subcategories:
                converted_subcategories, id_counter = self.convert_categories(subcategories, id_counter)
                converted_data[category_name] = converted_subcategories
            else:
                linkto_id = category.get('LinkTo')
                if linkto_id is not None:
                    converted_data[category_name] = {'name': linkto_id, 'id': id_counter}
                    id_counter += 1
                else:
                    continue

        return converted_data, id_counter

    def get_category(self, id, categories=None):
        if categories is None:
            categories = self.categories

        for cat, value in categories.items():
            if isinstance(value, dict):
                if 'id' in value and value['id'] == id:
                    return value['name']

                subcategory_result = self.get_category(id, value)
                if subcategory_result:
                    return subcategory_result

    def load_session(self):
        self.s = Session()
        self.s.headers['User-Agent'] = generate_user_agent()
        self.s.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        self.s.headers['Accept-Encoding'] = 'gzip, deflate, br'
        self.s.headers['Accept-Language'] = 'ru-RU,ru;q=0.9,kk-KZ;q=0.8,kk;q=0.7,en-US;q=0.6,en;q=0.5'

        r = self.s.get('https://www.wolframalpha.com/input/wpg/categories.jsp?load=true').json()
        self.categories, _ = self.convert_categories(r['Categories']['Categories'])
        self.API = r['domain']

    def check_problem(self, problem, answer):
        lvl = problem['difficulty']
        pid = problem['id']
        machine = problem['machine']
        for c in problem['session']:
            cookie = create_cookie(name=c['name'], value=c['value'], domain=c['domain'])
            self.s.cookies.set_cookie(cookie)

        url = f'{self.API}/input/wpg/checkanswer.jsp'

        params = {
            'attempt': 1,
            'difficulty': lvl,
            'load': 'true',
            'problemID': pid,
            'query': answer,
            's': machine,
            'type': 'InputField'
        }

        r = self.s.get(url, params=params).json()
        return {'correct': r['correct'], 'hint': r['hint'], 'solution': r['solution'], 'attempt': r['attempt']}

    def generate_problem(self, lvl=0, type='IntegerAddition'):
        lvl = {0: 'Beginner', 1: 'Intermediate', 2: 'Advanced'}[lvl]

        url = f'{self.API}/input/wpg/problem.jsp'

        params = {
            'count': 1,
            'difficulty': lvl,
            'load': 'true',
            'type': type
        }

        r = self.s.get(url, params=params).json()

        problems = r['problems']
        machine = r['machine']
        cookies = []
        for c in self.s.cookies:
            if c.name == 'JSESSIONID':
                cookies.append({'name': c.name, 'value': c.value, 'domain': c.domain})
        problem = problems[0]
        return {'text': problem['string_question'], 'image': problem['problem_image'], 'difficulty': lvl, 'id': problem['problem_id'], 'machine': machine, 'session': cookies}