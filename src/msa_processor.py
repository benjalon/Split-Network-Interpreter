# pylint: disable=no-member
'''Class which takes nexus file path and produces a
 processed & coloured MSA.'''
import re
import operator
import time
import concurrent.futures
from nexus import NexusReader
from numpy import empty
from numpy import zeros


class MsaProcessor():
    '''Processes a nexus file.'''

    def __init__(
            self, file_path, threading=True, top_splits=None, upper_limit=80,
            metric="Rand"):
        nexus_file = NexusReader(file_path)

        # Set class variables from file.
        self._msa = nexus_file.characters.matrix
        self.num_columns = nexus_file.characters.nchar
        self.num_species = nexus_file.characters.ntaxa
        self.species_names = nexus_file.characters.taxa
        self.symbols = nexus_file.characters.symbols
        self.upper_limit = upper_limit
        self.metric = metric

        # If set, only process top x splits sorted by weight.
        total_splits = self._process_splits(
            nexus_file.splits.block)
        total_splits = sorted(
            total_splits,
            key=operator.itemgetter('split_weight'), reverse=True)

        if top_splits is None:
            self.splits = total_splits
            self.num_splits = len(total_splits)
        else:
            self.splits = total_splits[0:top_splits]
            self.num_splits = top_splits

        # If the msa is 'assuming values' we must fill them in.
        if '.' in self.symbols:
            self._fix_msa()

        # Calculate the splits in each partition.
        self.split_by_column = None
        self.threading = threading

    def _fix_msa(self):
        msa_copy = self._msa

        # For each column make an array and add it to the main return msa
        for column in range(self.num_columns):
            for i, species in enumerate(self._msa):
                if i == 0:
                    top_base = self._msa[species][column]
                if self._msa[species][column] == '.':
                    msa_copy[species][column] = top_base
                else:
                    msa_copy[species][column] = self._msa[species][column]

        self._msa = msa_copy

    def _process_splits(self, block):
        '''
        Returns list containing dictionaries containing information on each
        split.
        '''
        split_list = []

        for data_row in block:

            # Rows that contain splits start with [n...
            if data_row[0] == "[":

                # Regex rule that gets three groups from:
                #   [7, size=1] 	 0.02142	  1 3 5 9,
                #    = ["7", "0.02124", "1 3 5 9"]
                reg = r"\[(.*),.*TAB\s(.*)\sTAB\s*(.*),"
                data_row = data_row.replace("\t", "TAB")
                split = re.findall(reg, data_row)
                splits_int = list(map(int, split[0][2].split(" ")))

                # Put into a dictionary in the correct types.
                split_dict = {
                    'split_number': int(split[0][0]),
                    'split_weight': float(split[0][1]),
                    'split': splits_int,
                    'inverse': self._get_inverse_split(splits_int)
                }
                split_list.append(split_dict)

        return split_list

    def _get_inverse_split(self, split):
        '''
        Returns the inverse of a partition
        e.g. Species = 6 Partiton = [1,2,3,5] Inverse = [4,6]
        '''
        item = list(range(1, self.num_species + 1))
        return list(set(item) - set(split))

    @staticmethod
    def _make_sets_from_column(column):
        '''
        Returns a partition of the column of bases or proteins.
        '''
        # In the dictionary each unique 'base' is stored as the key and each
        # column with the same 'base' is added to that key.
        set_dict = {}
        for i, base in enumerate(column):
            set_dict.setdefault(base, None)
            if set_dict[base] is None:
                set_dict[base] = [i]
            else:
                set_dict[base].append(i)

        # To create a list that looks more like the splits remove the 'base'
        # key and return a list of columns by 'base'. Add 1 to line up with
        # actual splits.
        temp = []
        for ind in set_dict:
            arr = set_dict[ind]
            arr = map(lambda x: x+1, arr)
            temp.append(list(arr))
        return temp

    def _rand_distance(self, partition_p, partition_q):
        '''Returns the distance by rand index between bases p and q'''
        rand_s = rand_r = rand_u = rand_v = 0

        # Go through every possible pairs between partitions.
        for i in range(1, self.num_species+1):
            for j in range(1, self.num_species+1):
                if i != j:
                    # Generate results for how values appear across both
                    # partitions.
                    set_info = self._part_sep(partition_p, partition_q, i, j)

                    if(set_info['pTogether'] and set_info['qTogether']):
                        rand_s += 1
                    if (not set_info['pTogether'] and not
                            set_info['qTogether']):
                        rand_r += 1
                    if (not set_info['pTogether'] and set_info['qTogether']):
                        rand_u += 1
                    if (set_info['pTogether'] and not set_info['qTogether']):
                        rand_v += 1

        # Use Rand Index to calculate distance between partitions.
        rand = (rand_r+rand_s)/(rand_r+rand_s+rand_u+rand_v)
        return rand

    @staticmethod
    def _part_sep(partition_p, partition_q, value_x, value_y):
        '''
        Returns a dictionary showing if p and q are together or separate in
        the two partitions
        '''
        return_dict = {}

        for part in partition_p:
            if(part.count(value_x) > 0 and part.count(value_y) > 0):
                return_dict['pTogether'] = True
                break
            else:
                return_dict['pTogether'] = False

        for part in partition_q:
            if(part.count(value_x) > 0 and part.count(value_y) > 0):
                return_dict['qTogether'] = True
                break
            else:
                return_dict['qTogether'] = False

        return return_dict

    def _match_split(self, partition):
        '''Matches a partition to the closest split'''
        score_list = []  # A list to keep track of rand scores.

        # For each split work out how close it is to the partition.
        for split in self.splits:
            # Combine split with other half.
            full_split = [split['split'], split['inverse']]

            if self.metric == "Rand":
                distance = self._rand_distance(full_split, partition)
            elif self.metric == "Jaccard":
                pass

            split_result = {
                'split_number': split['split_number'],
                'split_score': distance,
                'split_weight': split['split_weight']
            }
            score_list.append(split_result)

        # Sort the lists by score then weight to settle conflicts.
        score_list = sorted(
            score_list,
            key=operator.itemgetter(
                'split_score', 'split_weight'), reverse=True)

        # Return the position of the highest scoring split.
        if score_list[0]['split_number'] >= self.upper_limit:
            return score_list[0]['split_number']
        else:
            return False

    def _calculate(self, threading=True):
        '''
        Generates the results for the MSA.

        Args:
            threading (boolean): If Multi-threading should be used.
        '''
        start = time.time()  # Time monitor

        # Make a list to iterate through all the columns of the MSA.
        total_columns = list(range(self.num_columns))

        column_split = empty(self.num_columns, int)

        # If multi-threading is required use a ProcessPoolExecutor to carry
        # out multiple operations in an asynchronous manner.
        if threading:
            with concurrent.futures.ProcessPoolExecutor() as executor:
                for col_num, result in zip(
                        total_columns, executor.map(
                            self._calculate_column, total_columns)):

                    column_split[col_num] = result
        else:
            for col_num in total_columns:
                column_split[col_num] = self._calculate_column(col_num)

        total_time = time.time() - start
        print("Processing time = ", total_time)
        return column_split

    def _calculate_column(self, col_num):
        '''
        For a given column, match it with the closest split.
        '''
        # Get the column of the MSA.
        column = []
        for species in self._msa:
            column.append(self._msa[species][col_num])

        # As we use a Set, if there are any duplicates, the length will
        # greater than 1 meaning the column is a partition.
        if len(set(column)) > 1:

            # Now make the column into a parition referencing species
            # number. e.g. (A, A, G, A) would be (1,2,4) - (3)
            partition = self._make_sets_from_column(column)

            # Match the parition with the closest split.
            result = self._match_split(partition)
            if result is not False:
                return result
            return 0
        else:
            return 0

    def msa(self):
        '''
        Returns the MSA as a matrix.
        e.g.0{a,a,a,a},
            1{a,a,c,a}
        '''
        arra = empty([self.num_columns, self.num_species], str)
        # For each column make an array and add it to the main return msa
        for column in range(self.num_columns):
            for i, species in enumerate(self._msa):
                arra[column][i] = self._msa[species][column]

        return arra

    def split_columns(self):
        '''Returns an array containing the split found at each location.'''
        return self.split_by_column

    def process_msa(self):
        '''Processes the MSA and assigns it to object variable'''
        try:
            self.split_by_column = self._calculate(self.threading)
            return True
        except:
            print("There was an error processing the MSA.")
            return False
