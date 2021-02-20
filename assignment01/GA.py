# Mutation:

def swap_mutation(genotype):
    """Performs a swap mutation on a permutation genotype
    
    Pick two alleles at random and swap their positions
    
    Args:
        genotype: A genotype in a permutation format
        
    Returns:
        The genotype after the mutation    
    """
    locuses = np.random.choice(len(genotype), 2, replace=False)
    genotype[locuses[0]], genotype[locuses[1]] = genotype[locuses[1]], genotype[locuses[0]]
    return genotype

def insert_mutation(genotype):
    """Performs an insert mutation on a permutation genotype
    
    Pick two allele values at random and move the second to follow the first, shifting the rest
    
    Args:
        genotype: A genotype in a permutation format
        
    Returns:
        The genotype after the mutation    
    """
    locuses = np.random.choice(len(genotype), 2, replace=False)
    genotype.insert(locuses[0], genotype.pop(locuses[1]))
    return genotype

def scramble_mutation(genotype):
    """Performs a scramble mutation on a permutation genotype
    
    Pick a subset of genes at random, and randomly rearrange the alleles in those positions
    
    Args:
        genotype: A genotype in a permutation format
        
    Returns:
        The genotype after the mutation    
    """
    genotype_copy = genotype.copy()
    locuses = np.random.choice(len(genotype), np.random.randint(2, len(genotype)), replace=False)
    locuses_list = locuses.tolist()
    for locus in locuses:
        if len(locuses_list) == 1:
            genotype[locus] = genotype_copy[locuses_list[0]]
        else:
            genotype[locus] = genotype_copy[locuses_list.pop(np.random.randint(0, len(locuses_list)))]
        
    return genotype

def inversion_mutation(genotype):

    """Performs an inversion mutation on a permutation genotype
    
    Pick two alleles at random and then invert the substring between them
    
    Args:
        genotype: A genotype in a permutation format
        
    Returns:
        The genotype after the mutation    
    """
    locuses = np.random.choice(len(genotype), 2, replace=False)
    genotype[locuses[0]:locuses[1]+1] = genotype[locuses[0]:locuses[1]+1][::-1]
    return genotype

# Recombination:

def pmx(a, b, start, stop):
    child = [None]*len(a)
    
    # Copy a slice from first paret:
    child[start:stop] = a[start:stop]
    
    # Map the same slice in parent b to child using indices from parent a:
    for ind, x in enumerate(b[start:stop]):
        ind += start
        if x not in child:
            while child[ind] != None:
                ind = b.index(a[ind])
            child[ind] = x
    # Copy over the rest from parent b
    for ind, x in enumerate(child):
        if x == None:
            child[ind] = b[ind]
            
    return child

def pmx_pair(a, b):
    half = len(a) // 2
    start = np.random.randint(0, len(a)-half)
    stop = start+half
    return pmx(a, b, start, stop), pmx(b, a, start, stop)


def order_crossover(a, b, start, stop):
    child = [None]*len(a)
    
    # Copy a slice from first parent:
    child[start:stop] = a[start:stop]
    
    # Fill using order from second parent:
    b_ind = stop
    c_ind = stop
    l = len(a)
    while None in child:
        if b[b_ind % l] not in child:
            child[c_ind % l] = b[b_ind % l]
            c_ind += 1
        b_ind += 1
        
    return child

def order_crossover_pair(a, b):
    half = len(a) // 2
    start = np.random.randint(0, len(a)-half)
    stop = start + half
    return order_crossover(a, b, start, stop), order_crossover(b, a, start, stop)


def cycle_crossover(a, b):
    child = [None]*len(a)
    while None in child:
        ind = child.index(None)
        indices = []
        values = []
        while ind not in indices:
            val = a[ind]
            indices.append(ind)
            values.append(val)
            ind = a.index(b[ind])
        for ind, val in zip(indices, values):
            child[ind] = val
        a, b = b, a
        
    return child

def cycle_crossover_pair(a, b):
    return cycle_crossover(a, b), cycle_crossover(b, a)

##