
import time, random

interval = 1/1
max_questions = 2
time_question = 2
time_answer = 2
colors = ['#EE82EE', '#90EE90', '#87CEFA', '#FF4500']

def init(gameState, players):

    gameState['iteration'] = 0
    gameState['game'] = 'quiz'

    gameState['state'] = 'answer'
    gameState['countdown'] = 0
    gameState['questions_done'] = -1
    gameState['completed'] = []
    gameState['question'] = {}
    gameState['total_questions'] = max_questions

    gameState['players'] = []
    for index, player in enumerate(players):
        gameState['players'].append({'sid': player, 'score': 0, 'color': colors[index], 'selected': 0})

    return gameState

def update(gameState, players_movement, lastTick):

    deltaTime = (int(round(time.time() * 1000000)) - lastTick)/1000000

    gameState['iteration'] = gameState['iteration'] + 1

    gameState['countdown'] = gameState['countdown'] - 1

    if gameState['state'] == 'question' and gameState['countdown'] <= 0:
        gameState['state'] = 'answer'
        gameState['countdown'] = time_answer

        for player in gameState['players']:
            if player['selected'] == gameState['question']['correct']:
                player['score'] = player['score'] + 1

    elif gameState['state'] == 'answer' and gameState['countdown'] <= 0:
        gameState['state'] = 'question'
        gameState['countdown'] = time_question
        gameState['questions_done'] = gameState['questions_done'] + 1
        gameState = getNewQuestion(gameState)
        for player in gameState['players']:
            player['selected'] = 0

    return gameState

def ended(gameState):
    ended = False

    if gameState['questions_done'] >= max_questions:
        ended = True

    return ended

def getPlayerState(gameState, sid):
    for player in gameState['players']:
        if player['sid'] == sid:
            if gameState['state'] == 'answer':
                return {
                    'backgroundcolor': player['color'],
                    'quiz': {
                        'answers': gameState['question']['alternatives'],
                        'selected': player['selected'],
                        'questionnumber': gameState['questions_done'],
                        'totalquestions': max_questions,
                        'correctanswer': gameState['question']['correct']
                    }
                }
            else:
                return {
                    'backgroundcolor': player['color'],
                    'quiz': {
                        'answers': gameState['question']['alternatives'],
                        'selected': player['selected'],
                        'questionnumber': gameState['questions_done'],
                        'totalquestions': max_questions
                    }
                }
    return {}

def getNewQuestion(gameState):
    index = random.randint(0, len(quiz)-1)
    while index in gameState['completed']:
        index = random.randint(0, len(quiz)-1)

    gameState['completed'].append(index)
    gameState['question'] = quiz[index]

    return gameState

#http://www.pubquizarea.com/multiple-choice/general-knowledge-quiz/start/added/32/1/
quiz = [
    {
        'question': 'Who directed the 1983 film \'ET the Extra-Terrestrial\'?',
        'alternatives': [
            'Drew Barrymore',
            'Robin Williams',
            'Steven Spielberg',
            'Tom Hanks'
        ],
        'correct': 2
    },
    {
        'question': 'What is the highest point on the Earth\'s continental crust?',
        'alternatives': [
            'Annapurna',
            'K2',
            'Lhotse',
            'Mount Everest'
        ],
        'correct': 3,
        'funfact': 'There are 14 mountains over 8,000 m (26,427 feet) above sea level and they are all in the Himalaya and Karakoram ranges of Asia'
    },
    {
        'question': 'Which two colours make purple?',
        'alternatives': [
            'Blue and Yellow',
            'Green and Orange',
            'Red and Blue',
            'Red and Green'
        ],
        'correct': 2
    },
    {
        'question': 'What is the square root of 9?',
        'alternatives': [
            '1',
            '3',
            '27',
            '81'
        ],
        'correct': 1
    },
    {
        'question': 'Which musical family does the saxophone belong to?',
        'alternatives': [
            'Jazz',
            'Percussion',
            'Strings',
            'Woodwind'
        ],
        'correct': 0
    },
    {
        'question': 'Which racecourse hosts the Grand National?',
        'alternatives': [
            'Aintree',
            'Epsom',
            'Goodwood',
            'Sandown'
        ],
        'correct': 0
    },
    {
        'question': 'In the Bible, who betrayed Jesus?',
        'alternatives': [
            'Abraham',
            'Jonah',
            'Judas',
            'Samson'
        ],
        'correct': 2,
        'funfact': 'In the Gospel of John, Judas carried the disciples\' money bag and betrayed Jesus for a bribe of \'thirty pieces of silver\' by identifying him with a kiss'
    },
    {
        'question': 'Which fruits are most commonly used to make wine?',
        'alternatives': [
            'Grapes',
            'Lemons',
            'Oranges',
            'Strawberries'
        ],
        'correct': 0
    },
    {
        'question': 'Which Italian city has a famous leaning tower?',
        'alternatives': [
            'Florence',
            'Pisa',
            'Rome',
            'Venice'
        ],
        'correct': 1,
        'funfact': 'The 4 degree lean means that the top of the tower is 3.9 metres (12ft 10in) from where it would stand if the tower were perfectly vertical'
    },
    {
        'question': 'Which tree grows from an acorn?',
        'alternatives': [
            'Ash',
            'Elm',
            'Lime',
            'Oak'
        ],
        'correct': 3
    }
]
