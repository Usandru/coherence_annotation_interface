import annotator
import constants

class composite:

    def __init__(self, list_of_annotator_objects):
        self.id_to_id_dict = dict()
        self.id_pairs = set()

        for annotator_object in list_of_annotator_objects:
            for i in range(annotator_object.number_of_annotations):
                right = annotator_object.right_id[i]
                r_int_id = int(right.split(" ")[0])
                left = annotator_object.left_id[i]
                l_int_id = int(left.split(" ")[0])
                direction = annotator_object.coherence_direction[i]

                if r_int_id < l_int_id:
                    pair = (right, left)
                else:
                    pair = (left, right)

                self.id_pairs.add(pair)

                if right not in self.id_to_id_dict:
                    self.id_to_id_dict[right] = {left : 0}
                else:
                    if left not in self.id_to_id_dict[right]:
                        self.id_to_id_dict[right][left] = 0
                if left not in self.id_to_id_dict:
                    self.id_to_id_dict[left] = {right : 0}
                else:
                    if right not in self.id_to_id_dict[left]:
                        self.id_to_id_dict[left][right] = 0

                if direction == constants.RIGHT:
                    self.id_to_id_dict[right][left] += 1
                else:
                    self.id_to_id_dict[left][right] += 1
    
    def agreement(self):
        pair_agreement = list()
        for pair in self.id_pairs:
            first = self.id_to_id_dict[pair[0]][pair[1]]
            second = self.id_to_id_dict[pair[1]][pair[0]]
            pair_agreement.append((pair, first, second))

        return pair_agreement