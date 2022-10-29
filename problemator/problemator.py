from requests import Session, get
from user_agent import generate_user_agent


def loadCategories():
    global categories
    categories = {}
    r = get('https://www.wolframalpha.com/input/wpg/categories.jsp?load=true',
            headers={'User-Agent': generate_user_agent()}).json()
    i = 0
    for c in r['Categories']['Categories']:
        sec = c['Display']
        categories[sec] = dict()
        for sb in c['Subcategories']:
            categories[sec][sb['Display']] = dict()
            for sbb in sb['Subcategories']:
                categories[sec][sb['Display']][sbb['Display']] = {'type': sbb['LinkTo'], 'id': i}
                i += 1


def getCategories():
    global categories
    return categories


def getCategoryByID(id):
    for cat in categories:
        for c in categories[cat]:
            for cc in categories[cat][c]:
                if id == categories[cat][c][cc]['id']:
                    return categories[cat][c][cc]['type']
    return None


def getCategoryByName(name):
    for cat in categories:
        for c in categories[cat]:
            for cc in categories[cat][c]:
                if name == cc:
                    return categories[cat][c][cc]['type']
    return None


def loadSession():
    global API, s
    loadCategories()
    s = Session()
    s.headers['User-Agent'] = generate_user_agent()
    s.headers[
        'Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    s.headers['Accept-Encoding'] = 'gzip, deflate, br'
    s.headers['Accept-Language'] = 'ru-RU,ru;q=0.9,kk-KZ;q=0.8,kk;q=0.7,en-US;q=0.6,en;q=0.5'

    API = s.get('https://www.wolframalpha.com/input/wpg/categories.jsp?load=true').json()['domain']


def generateProblem(lvl=0, type='IntegerAddition', count=1):
    lvl = {0: 'Beginner', 1: 'Intermediate', 2: 'Advanced'}[lvl]
    problems = s.get(f'{API}/input/wpg/problem.jsp?count={count}&difficulty={lvl}&load=1&type={type}').json()[
        'problems']
    return [{'text': problem['string_question'], 'image': problem['problem_image']} for problem in problems]
