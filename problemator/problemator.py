from requests import Session, get
from requests.cookies import create_cookie
from user_agent import generate_user_agent

categories = {}


def searchCategories(cats):
    global categories
    for c in cats:
        if 'Subcategories' in c:
            searchCategories(c['Subcategories'])
        else:
            categories[c['LinkTo']] = len(categories)


def getCategories():
    return categories


def getCategory(id):
    for cat in categories.keys():
        if categories[cat] == id:
            return cat


def loadSession():
    global API, s
    s = Session()
    s.headers['User-Agent'] = generate_user_agent()
    s.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    s.headers['Accept-Encoding'] = 'gzip, deflate, br'
    s.headers['Accept-Language'] = 'ru-RU,ru;q=0.9,kk-KZ;q=0.8,kk;q=0.7,en-US;q=0.6,en;q=0.5'

    r = s.get('https://www.wolframalpha.com/input/wpg/categories.jsp?load=true').json()
    searchCategories(r['Categories']['Categories'])
    API = r['domain']

def checkProblem(problem, answer):
    lvl = problem['difficulty']
    pid = problem['id']
    machine = problem['machine']
    for c in problem['session']:
        cookie = create_cookie(name=c['name'], value=c['value'], domain=c['domain'])
        s.cookies.set_cookie(cookie)
    r = s.get(f'{API}/input/wpg/checkanswer.jsp?attempt=1&difficulty={lvl}&load=true&problemID={pid}&query={answer}&s={machine}&type=InputField').json()
    return {'correct': r['correct'], 'hint': r['hint'], 'solution': r['solution']}


def generateProblem(lvl=0, type='IntegerAddition'):
    lvl = {0: 'Beginner', 1: 'Intermediate', 2: 'Advanced'}[lvl]
    r = s.get(f'{API}/input/wpg/problem.jsp?count=1&difficulty={lvl}&load=1&type={type}').json()
    problems = r['problems']
    machine = r['machine']
    cookies = []
    for c in s.cookies:
        if c.name == 'JSESSIONID':
            cookies.append({'name': c.name, 'value': c.value, 'domain': c.domain})
    problem = problems[0]
    return {'text': problem['string_question'], 'image': problem['problem_image'], 'difficulty': lvl, 'id': problem['problem_id'], 'machine': machine, 'session': cookies}
