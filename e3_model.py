'''
Created on Nov 22, 2016

'''
from pinject import copy_args_to_public_fields
import hashlib

class Tap(object):
    @copy_args_to_public_fields
    def __init__(self, isCoverage, isSiblingDisjointness, regions, taxonomyA, taxonomyB, articulations):
        pass
    def add_articulation(self, articulation):
        self.articulations.append(articulation)
    def remove_articulation(self, articulationIndex):
        del self.articulations[int(articulationIndex)]
    def __str__(self, *args, **kwargs):
        indices = ['']
        for x in range(1, len(self.articulations)):
            indices.append(str(x) + ". ")
        articulationLines = [x + y for x, y in zip(indices, self.articulations)]
        indices = ['']
        for x in range(1, len(self.taxonomyA)):
            indices.append(str(x) + ". ")
        taxonomyALines = [x + y for x, y in zip(indices, self.taxonomyA)]
        indices = ['']
        for x in range(1, len(self.taxonomyB)):
            indices.append(str(x) + ". ")
        taxonomyBLines = [x + y for x, y in zip(indices, self.taxonomyB)]
        return ('isCoverage:' + str(self.isCoverage) + '\nisSiblingDisjontness:' + str(self.isSiblingDisjointness) + '\nRegions:' + self.regions + '\n' + 
                '\n\n'.join(['\n'.join(taxonomyALines), '\n'.join(taxonomyBLines), '\n'.join(articulationLines)]))
    def get_id(self):
        return hashlib.sha1(self.__str__()).hexdigest()
    
#could be a graph at some point if desired to be able to modify the taxonomy on the fly
#e.g. adding a new child somewhere
class Taxonomy(object):
    @copy_args_to_public_fields
    def __init__(self, cleantax):
        pass

#see Taxonomy comment
class Articulation(object):
    @copy_args_to_public_fields
    def __init__(self, cleantax):
        pass
