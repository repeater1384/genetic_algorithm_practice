import string
import random


def print_info():
    print('-----유전 알고리즘을 이용한 단어 학습-----')
    print('-----------------------------0512, v1 ')
    print()
    print()


PASSWORD = input('비밀번호를 설정해주세요 : ')
MIN_LEN = 2  # 예측할 단어의 최소 길이
MAX_LEN = 50  # 예측할 단어의 최대 길이
GENERATION_SIZE = 100  # 한 세대당 단어 개수(모델 성능에 가장 큰 영향)
SURVIVOR_NUM = 25  # 단어의 성능 순으로 정렬 후 ,다음 세대로 넘어갈 단어 개수
LUCKY_NUM = 15  # 운좋게 다음 세대로 넘어갈 다음 개수
MUTATE_PROB = 0.1  # 자식 만들때 돌연변이 생길 확률

if input('Hyper Parameter를 설정하시겠습니까? (Y/N) : ') == 'Y':
    while True:
        try:
            MIN_LEN = int(input('예측할 단어의 최소 길이 : '))
            MAX_LEN = int(input('예측할 단어의 최대 길이 : '))
            GENERATION_SIZE = int(input('한 세대당 단어 개수 : '))
            SURVIVOR_NUM = int(input('단어의 성능 순으로 정렬 후 ,다음 세대로 넘어갈 단어 개수 : '))
            LUCKY_NUM = int(input('운좋게 다음 세대로 넘어갈 다음 개수 : '))
            MUTATE_PROB = int(input('자식 만들때 돌연변이 생길 확률 : '))
            break
        except:
            print("정수만 입력해주세요")
print('\nMIN_LEN :', MIN_LEN, '\nMAX_LEN :', MAX_LEN, '\nGENERATION_SIZE :', GENERATION_SIZE, '\nSURVIVOR_NUM :',
      SURVIVOR_NUM, '\nLUCKY_NUM :', LUCKY_NUM, '\nMUTATE_PROB :', MUTATE_PROB)

input("\nPress Enter")


def generate_word(length):
    """length의 길이를 가지는 랜덤 단어를 return"""
    all_word = string.ascii_letters + string.digits
    return ''.join(random.sample(all_word, k=length))


def get_first_population(size=GENERATION_SIZE, min_len=MIN_LEN, max_len=MAX_LEN):
    """(min_len, max_len) 사이의 길이를 가지는 size개의 단어로 이루어진 리스트를 return"""
    population = [generate_word(random.randint(min_len, max_len + 1)) for _ in range(size)]
    return population


def cal_fitness(guess_word, password=PASSWORD):
    """한 단어를 input으로 받고, 단어와 PASSWORD의 일치도를 return"""
    fitness_score = 0

    # 단어 길이 다르면 -2부터 시작
    if len(guess_word) != len(password): fitness_score -= 2

    for idx in range(min(len(password), len(guess_word))):
        if password[idx] == guess_word[idx]:
            fitness_score += 1

    return round(fitness_score / len(password) * 100, 3)


def select_survivor(population, survivor_num=SURVIVOR_NUM, lucky_num=LUCKY_NUM):
    """한 세대를 input으로 받고, (단어, 점수)로 이루어진 리스트를 점수의 내림차순으로 정렬
    정렬된 리스트를 기준으로, survivor_num + lucky_num 개수의 단어를 return """

    performance_score_list = sorted([(pop, cal_fitness(pop)) for pop in population], key=lambda x: -x[1])
    survivor_list = [*random.sample(population, k=lucky_num)]
    for i in range(survivor_num):
        survivor_list.append(performance_score_list[i][0])

    return survivor_list


def mutate_word(word, mutate_prob=MUTATE_PROB):
    """mutation_prob의 확률로 랜덤한 한 자리를 랜덤 문자로 바꿔서 return"""
    word = [*word]
    if random.random() < mutate_prob:
        idx = random.randint(0, len(word) - 1)
        word[idx] = generate_word(1)
    return ''.join(word)


def create_child(father, mother):
    child = ''

    # 50% 확률로 엄마 길이에 아빠를 맞춤
    if random.random() > 0.5:
        while len(father) < len(mother):
            father += generate_word(1)
    # 반대로 아빠 길이에 엄마를 맞춤
    else:
        while len(father) > len(mother):
            mother += generate_word(1)

    for i in range(min(len(father), len(mother))):
        if random.random() > 0.5:
            child += father[i]
        else:
            child += mother[i]

    return child


def get_next_generation(old_population, size=GENERATION_SIZE):
    """old_population 받고, survivor_list 구해, 교배시킨 후
    mutate_word 한번씩 적용한 뒤 생긴 next_population return"""

    next_population = []
    survivor_list = select_survivor(old_population)
    survivor_num = len(survivor_list)

    for idx in range(survivor_num // 2):
        father, mother = survivor_list[idx], survivor_list[survivor_num - idx - 1]

        for _ in range(size // (survivor_num // 2)):
            child = mutate_word(create_child(father, mother))
            next_population.append(child)

    return next_population


if __name__ == "__main__":
    cur_population = get_first_population()
    generation = 1

    while True:
        population_repr_word = cur_population[0]  # 해당 세대에서 가장 성능좋은 단어
        population_score = cal_fitness(cur_population[0])  # 가장 성능 좋은 단어의 점수
        print(f'#Gen{generation} : {population_repr_word} {population_score}')

        if population_score == 100:
            break

        cur_population = get_next_generation(cur_population)
        generation += 1

input('Press Enter')