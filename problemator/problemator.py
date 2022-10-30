from requests import Session, get
from user_agent import generate_user_agent

categories = {}
i = 0

def searchCategories(cats):
    global categories, i
    for c in cats:
        if 'Subcategories' in c:
            searchCategories(c['Subcategories'])
        else:
            categories[c['LinkTo']] = {'name': c['Display'], 'id': i}
            i += 1

def loadCategories():
    r = get('https://www.wolframalpha.com/input/wpg/categories.jsp?load=true',
            headers={'User-Agent': generate_user_agent()}).json()
    searchCategories(r['Categories']['Categories'])


def getCategories():
    return categories


def getCategoryByID(id):
    for cat in categories.keys():
        if id == categories[cat]['id']:
            return cat
    return None


def getCategoryByName(name):
    for cat in categories.keys():
        if name == categories[cat]['name']:
            return cat
    return None


def loadSession():
    global API, s
    loadCategories()
    s = Session()
    s.headers['User-Agent'] = generate_user_agent()
    s.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    s.headers['Accept-Encoding'] = 'gzip, deflate, br'
    s.headers['Accept-Language'] = 'ru-RU,ru;q=0.9,kk-KZ;q=0.8,kk;q=0.7,en-US;q=0.6,en;q=0.5'

    API = s.get('https://www.wolframalpha.com/input/wpg/categories.jsp?load=true').json()['domain']


def generateProblems(lvl=0, type='IntegerAddition', count=1):
    lvl = {0: 'Beginner', 1: 'Intermediate', 2: 'Advanced'}[lvl]
    r = s.get(f'{API}/input/wpg/problem.jsp?count={count}&difficulty={lvl}&load=1&type={type}').json()
    problems = r['problems']
    machine = r['machine']
    arr = []
    for problem in problems:
        pid = problem['problem_id']
        r = s.get(f'https://www6b3.wolframalpha.com/input/wpg/checkanswer.jsp?attempt=1&difficulty={lvl}&load=true&problemID={pid}&query=const&s={machine}&type=InputField').json()
        arr.append({'problem': {'text': problem['string_question'], 'image': problem['problem_image']}, 'hint': r['hint'], 'solution': r['solution']})
    return arr
