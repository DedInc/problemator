from requests import Session, get
from requests.cookies import create_cookie
from user_agent import generate_user_agent


class Problemator:
    def __init__(self):
        self.categories = {}
        self.load_session()

    def search_categories(self, cats):
        for c in cats:
            if 'Subcategories' in c:
                self.search_categories(c['Subcategories'])
            else:
                self.categories[c['LinkTo']] = len(self.categories)

    def get_category(self, id):
        for cat in self.categories.keys():
            if self.categories[cat] == id:
                return cat

    def load_session(self):
        self.s = Session()
        self.s.headers['User-Agent'] = generate_user_agent()
        self.s.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        self.s.headers['Accept-Encoding'] = 'gzip, deflate, br'
        self.s.headers['Accept-Language'] = 'ru-RU,ru;q=0.9,kk-KZ;q=0.8,kk;q=0.7,en-US;q=0.6,en;q=0.5'

        r = self.s.get('https://www.wolframalpha.com/input/wpg/categories.jsp?load=true').json()
        self.search_categories(r['Categories']['Categories'])
        self.API = r['domain']

    def check_problem(self, problem, answer):
        lvl = problem['difficulty']
        pid = problem['id']
        machine = problem['machine']
        for c in problem['session']:
            cookie = create_cookie(name=c['name'], value=c['value'], domain=c['domain'])
            self.s.cookies.set_cookie(cookie)
        r = self.s.get(f'{self.API}/input/wpg/checkanswer.jsp?attempt=1&difficulty={lvl}&load=true&problemID={pid}&query={answer}&s={machine}&type=InputField').json()
        return {'correct': r['correct'], 'hint': r['hint'], 'solution': r['solution']}

    def generate_problem(self, lvl=0, type='IntegerAddition'):
        lvl = {0: 'Beginner', 1: 'Intermediate', 2: 'Advanced'}[lvl]
        r = self.s.get(f'{self.API}/input/wpg/problem.jsp?count=1&difficulty={lvl}&load=1&type={type}').json()
        problems = r['problems']
        machine = r['machine']
        cookies = []
        for c in self.s.cookies:
            if c.name == 'JSESSIONID':
                cookies.append({'name': c.name, 'value': c.value, 'domain': c.domain})
        problem = problems[0]
        return {'text': problem['string_question'], 'image': problem['problem_image'], 'difficulty': lvl, 'id': problem['problem_id'], 'machine': machine, 'session': cookies}