"""Class which takes nexus file path and produces a
 processed & coloured MSA."""
import re
from nexus import NexusReader


class MsaProcessor():
    """Processes a nexus file."""

    def __init__(self, file_path):
        nexus_file = NexusReader(file_path)

        self.msa = nexus_file.characters.matrix  # pylint: disable=no-member
        self.num_characters = nexus_file.characters.nchar  # pylint: disable=no-member
        self.num_species = nexus_file.characters.ntaxa  # pylint: disable=no-member
        self.symbols = nexus_file.characters.symbols  # pylint: disable=no-member
        self.splits = self._process_splits(nexus_file.splits.block)  # pylint: disable=no-member

        self.calculate()

        # splits = getSplits(n.splits.block[6:-2])
        # colSplit = zeros([len(msa)],int)
        # i = 0
        # for col in msa:
        #     if (isPartition(col)):
        #         partition = getSets(col)
        #         colSplit[i] = matchSplit(partition, splits, n.taxa.ntaxa)
        #     else:
        #         colSplit[i] = 0
        #     i += 1
        # arr = {}
        # arr["msa"] = msa
        # arr["colSplit"] = colSplit
        # arr["n"] = n
        # arr["splits"] = splits

    def _process_splits(self, block):
        """Returns a list of splits e.g [1,2,3],[1],[3,4]"""

        split_list = []

        for data_row in block:
            if data_row[0] == "[":
                reg = r"\[(.*),.*TAB\s(.*)\sTAB\s*(.*),"
                data_row = data_row.replace("\t", "TAB")
                split = re.findall(reg, data_row)
                sp = list(map(int, split[0][2].split(" ")))
                split_dict = {
                    'split_number': int(split[0][0]),
                    'split_weight': float(split[0][1]),
                    'split': sp,
                    'inverse': self._get_inverse_split(sp)
                }
                split_list.append(split_dict)

        return split_list

    def _get_inverse_split(self, split):
        item = list(range(1, self.num_species + 1))
        return list(set(item) - set(split))

    def calculate(self):
        """Does the main logic"""
        # for col in msa:
        #     if (isPartition(col)):
        #         partition = getSets(col)
        #         colSplit[i] = matchSplit(partition, splits, n.taxa.ntaxa)
        #     else:
        #         colSplit[i] = 0
        #     i += 1
        for col_num in range(self.num_characters):

            # Get the column of the MSA.
            column = []
            for species in self.msa:
                column.append(species[col_num])

            if len(column) > 1:  # if is partition
                pass


PRO = MsaProcessor('/Users/benlonghurst/Documents/GitHub/Split-Network-Interpreter/Nexus_Examples/beesProcessed.nex')
