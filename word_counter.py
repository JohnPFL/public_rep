import re

class WordCounter:
    def __init__(self, dataset_a_path, dataset_b_path, output_path='output_result.txt'):
        self.dataset_a_path = dataset_a_path
        self.dataset_b_path = dataset_b_path
        self.output_path = output_path
        self.words_a = []
        self.counts_b = {}
        self.result = []

    def _preprocess_word(self, word):
        return re.sub(r'[^a-zA-Z]', '', word.strip().lower())

    def _read_dataset(self, file_path):
        with open(file_path, 'r') as file:
            return file.readlines()

    def _preprocess_dataset_a(self):
        self.words_c = [self._preprocess_word(line.split(',')[0]) for line in self._read_dataset(self.dataset_a_path)]
        self.words_sv = [self._preprocess_word(line.split(',')[1]) for line in self._read_dataset(self.dataset_a_path)]
        self.words_a = self.words_c + self.words_sv

    def _create_counts_dictionary(self):
        for line in self._read_dataset(self.dataset_b_path):
            parts = line.split()
            if len(parts) > 1:
                word_b = self._preprocess_word(parts[0])
                count_b = int(parts[1])
                self.counts_b[word_b] = count_b

    def _match_words_with_counts(self):
        data_a = self._read_dataset(self.dataset_a_path)[1:]  # Skip the header line
        for line in data_a:
            parts_a = line.split(',')
            word_a = self._preprocess_word(parts_a[0])
            word_b = self._preprocess_word(parts_a[1])
            category = self._preprocess_word(parts_a[2])
            count_a = self.counts_b.get(word_a, 0)
            count_b = self.counts_b.get(word_b, 0)
            self.result.append((word_a, count_a, word_b, count_b, category))

    def generate_output_file(self):
        with open(self.output_path, 'w') as output_file:
            output_file.write("cl_word,cl_count,spel_var,sv_count,category\n")
            for item in self.result:
                output_file.write(','.join(map(str, item)) + '\n')


    def process_datasets(self):
        self._preprocess_dataset_a()
        self._create_counts_dictionary()
        self._match_words_with_counts()
        self.generate_output_file()


# Example usage:
custom_output_path = 'custom_output_result.txt'
word_counter = WordCounter('word_list_human_ev.txt', '/hpc/uu_cs_nlpsoc/data/coling2020_nguyen_grieve/data/twitter/london_tweets_processed_may2018_april2019_vocab_count.txt', custom_output_path)
word_counter.process_datasets()
