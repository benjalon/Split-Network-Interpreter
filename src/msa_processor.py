# pylint: disable=no-member
"""Class which takes nexus file path and produces a
 processed & coloured MSA."""
import re
import operator
import time
import concurrent.futures
from nexus import NexusReader
from numpy import zeros


class MsaProcessor():
    """Processes a nexus file."""

    def __init__(self, file_path, top_splits=None):
        nexus_file = NexusReader(file_path)

        self._msa = nexus_file.characters.matrix
        self.num_columns = nexus_file.characters.nchar
        self.num_species = nexus_file.characters.ntaxa
        self.symbols = nexus_file.characters.symbols
        total_splits = self._process_splits(
            nexus_file.splits.block)
        self.upper_limit = 0
        total_splits = sorted(
            total_splits,
            key=operator.itemgetter('split_weight'), reverse=True)
        if top_splits is None:
            self.splits = total_splits
        else:
            self.splits = total_splits[0:top_splits]
        print("Total time: {}".format(self._calculate()))

    def _process_splits(self, block):
        """Returns a list of splits e.g [1,2,3],[1],[3,4]"""

        split_list = []

        for data_row in block:
            if data_row[0] == "[":
                reg = r"\[(.*),.*TAB\s(.*)\sTAB\s*(.*),"
                data_row = data_row.replace("\t", "TAB")
                split = re.findall(reg, data_row)
                splits_int = list(map(int, split[0][2].split(" ")))
                split_dict = {
                    'split_number': int(split[0][0]),
                    'split_weight': float(split[0][1]),
                    'split': splits_int,
                    'inverse': self._get_inverse_split(splits_int)
                }
                split_list.append(split_dict)

        return split_list

    def _get_inverse_split(self, split):
        item = list(range(1, self.num_species + 1))
        return list(set(item) - set(split))

    @staticmethod
    def _make_sets_from_column(column):
        """Returns two sets representing the partition in the MSA"""
        set_dict = {}
        i = 0
        for base in column:
            set_dict.setdefault(base, None)
            if set_dict[base] is None:
                set_dict[base] = [i]
            else:
                set_dict[base].append(i)
            i += 1

        temp = []
        for ind in set_dict:
            arr = set_dict[ind]
            arr = map(lambda x: x+1, arr)
            temp.append(list(arr))
        return temp

    def _rand_distance(self, partition_p, partition_q):
        """Returns the distance by rand index between bases p and q"""
        rand_s = rand_r = rand_u = rand_v = 0

        for i in range(1, self.num_species+1):
            for j in range(1, self.num_species+1):
                if i != j:
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
        rand = (rand_r+rand_s)/(rand_r+rand_s+rand_u+rand_v)
        return rand

    @staticmethod
    def _part_sep(partition_p, partition_q, value_x, value_y):
        """
        Returns a dictionary showing if p and q are together or separate in
        the two partitions
        """
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
        """Matches a partition to the closest split"""
        num = len(self.splits)
        score_list = zeros([num])
        i = 0

        for split in self.splits:
            full_split = [split['split'], split['inverse']]
            score_list[i] = self._rand_distance(full_split, partition)
            i += 1

        highest = 0
        for i, score in enumerate(score_list):
            if score > highest:
                highest = score
                pos = i+1

        return pos

    def _calculate(self, threading=True):
        """Does the main logic"""
        start = time.time()
        total_columns = list(range(self.num_columns))
        if threading:
            with concurrent.futures.ProcessPoolExecutor() as executor:
                for col_num, result in zip(
                        total_columns, executor.map(
                            self._calc2, total_columns)):

                    print("Column: {} - Result {}".format(col_num, result))
        else:
            for col_num in total_columns:
                print("Column: {} - Result {}".format(
                    col_num, self._calc2(col_num)))

        return time.time() - start

    def _calc2(self, col_num):
        # Get the column of the MSA.
        column = []
        for species in self._msa:
            column.append(self._msa[species][col_num])

        # As we use a Set, if there are any duplicates, the length will
        # greater than 1 meaning the column is a partition.
        if len(set(column)) > 1:

            # Now make the column into a parition referencing species
            # number. e.g. (1:A,2:A,3:G,4:A) would be (1,2,4) - (3)
            partition = self._make_sets_from_column(column)
            result = self._match_split(partition)
            return result
        else:
            return "N/A"

    def msa(self):
        """Returns the MSA as a matrix."""

    def split_columns(self):
        """Returns an array containing the split found at each location."""

PATH = '/Users/benlonghurst/Documents/GitHub/'
PATH = PATH + 'Split-Network-Interpreter/Nexus_Examples/'
PRO = MsaProcessor(PATH+'mammals.nex', 10)
