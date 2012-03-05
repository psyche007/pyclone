'''
Created on 2012-02-08

@author: Andrew Roth
'''
from collections import defaultdict

class DpSamplerPostProcessor(object):
    def __init__(self, data):       
        self.genes = data['genes']
        
        self._results = data['results']
        
    @property
    def alpha(self):
        return self._results['alpha']
    
    @property
    def cellular_frequencies(self):
        '''
        Returns a dictionary with keys genes, and values posterior samples of cellular frequencies.
        '''
        phi = defaultdict(list)
        
        labels = self._get_labels_by_gene()
        
        for gene in labels:
            for label, sample in zip(labels[gene], self._results['phi']):
                phi[gene].append(sample[label])
        
        return phi

    @property
    def num_components(self):
        '''
        Returns a list of the number of components used in by each MCMC sample.
        '''
        labels = self._results['labels']
        
        num_components = []
        
        for sample in labels:
            num_components.append(len(set(sample)))
        
        return num_components

    @property
    def similarity_matrix(self):
        '''
        Gets the posterior similarity matrix. The i,j entry is the number of times gene i and j where in the same
        cluster.
        '''            
        n = len(self.genes)
        
        sim_mat = [[0] * n for _ in range(n)] 
        
        labels = self._get_labels_by_gene()
        
        for i in range(n):
            for j in range(i, n):
                gene_1 = self.genes[i]
                gene_2 = self.genes[j]
                
                sim_mat[i][j] = self._get_gene_similarity(labels[gene_1], labels[gene_2])
                sim_mat[j][i] = sim_mat[i][j] 
        
        return sim_mat

    def _get_labels_by_gene(self):
        '''
        Returns a dict with keys genes, and values the class label of the genes for each MCMC sample.
        '''
        labels = defaultdict(list)
        
        for sample in self._results['labels']:
            for gene, label in zip(self.genes, sample):
                labels[gene].append(label)
        
        return labels

    def _get_gene_similarity(self, labels_1, labels_2):
        '''
        Computes how frequently items in two lists match.
        '''
        similarity = 0
        
        for l1, l2 in zip(labels_1, labels_2):
            if l1 == l2:
                similarity += 1
        
        return similarity

if __name__ == "__main__":
    post_processor = DpSamplerPostProcessor("../../examples/test.pickle")
    
    print post_processor.similarity_matrix
    print post_processor.num_components
