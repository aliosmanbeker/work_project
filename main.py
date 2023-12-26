import random
import yaml
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor
import datetime

class RandomNumberGenerator:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.count < self.y:
            number = random.randint(10 ** (self.x - 1), 10 ** self.x - 1)
            self.count += 1
            return number
        else:
            raise StopIteration

def save_file(file_name, random_number_generator, num_threads=64):
    with open(file_name, 'w') as file, ThreadPoolExecutor(max_workers=num_threads) as executor:
        for number in random_number_generator:
            executor.submit(file.write, str(number) + '\n')

def sum_numbers_from_file(file_name):
    total_sum = 0
    with open(file_name, 'r') as file:
        for line in file:
            try:
                number = int(line.strip())
                total_sum += number
            except ValueError as e:
                print(f"error: {e} - invalid value: {line.strip()}")

    return total_sum

def main():
    with open('config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)

    x = config['X']
    y = config['Y']
    z_file_name = config['Z']

    random_number_generator = RandomNumberGenerator(x, y)

    save_file(z_file_name, random_number_generator)

    pool = Pool(processes=10)
    chunks = [z_file_name] * 10
    results = pool.map(sum_numbers_from_file, chunks)
    pool.close()
    pool.join()

    total_sum = sum(results)
    print("Toplam: {}".format(total_sum))

if __name__ == "__main__":
    start_time = datetime.datetime.now()
    main()
    end_time = datetime.datetime.now()
    print("Total time: {}".format(end_time - start_time))
