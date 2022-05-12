import string
import random

PASSWORD = 'bluesky2'
GENERATION_SIZE = 100
SURVIVOR_NUM = 35
LUCKY_NUM = 5
MUTATE_PROB = 0.1


def generate_word(length):
    '''length의 길이를 가지는 랜덤 단어를 return'''
    all_word = string.ascii_letters + string.digits
    return ''.join(random.sample(all_word, k=length))


def get_first_population(size=GENERATION_SIZE, min_len=2, max_len=10):
    '''(min_len, max_len) 사이의 길이를 가지는 size개의 단어로 이루어진 리스트를 return'''
    population = [generate_word(random.randint(min_len, max_len + 1)) for _ in range(size)]
    return population


def cal_fitness(guess_word, password=PASSWORD):
    '''한 단어를 input으로 받고, 단어와 PASSWORD의 일치도를 return'''
    fitness_score = 0
    for idx in range(min(len(password), len(guess_word))):
        if password[idx] == guess_word[idx]:
            fitness_score += 1

    return round(fitness_score / len(password) * 100, 3)


def select_survivor(population, survivor_num=SURVIVOR_NUM, lucky_num=LUCKY_NUM):
    '''한 세대를 input으로 받고, (단어, 점수)로 이루어진 리스트를 점수의 내림차순으로 정렬
    정렬된 리스트를 기준으로, 상위 survivor_num 개수의 단어 + lucky_num 개수의 랜덤 단어를 리턴 '''

    performance_score_list = sorted([(pop, cal_fitness(pop)) for pop in population], key=lambda x: -x[1])
    survivor_list = [*random.sample(population, k=lucky_num)]
    for i in range(survivor_num):
        survivor_list.append(performance_score_list[i][0])

    return survivor_list


def mutate_word(word, mutate_prob=MUTATE_PROB):
    '''mutation_prob의 확률로 랜덤한 한 자리를 랜덤 문자로 바꿔서 return'''
    word = [*word]
    if random.random() < mutate_prob:
        idx = random.randint(0, len(word))
        word[idx] = generate_word(1)
    return ''.join(word)


def get_next_generation(old_population, size=GENERATION_SIZE):
    pass

select_survivor(get_first_population(100))
