#Author Mporras
#Date 13/sep/2018
from functools import reduce


def flatMap(f, l):
    '''
    flatMap:

    similar a map, pero cada elemento de entrada puede ser
    mapeado a 0 o mas elementos de salida, a si que la funcion f
    deberia de retornar una sequencia (lista o tupla) en vez de un
    simple elemento
    '''
    out = []
    for e in map(f, l):
        out.extend(list(e))
    return out


def reduceByKey(f, l):
    '''
    reduceByKey:
    esta se llama con listas de pares (K, V) y devuelve una lista
    de pares (K, V) donde los valores (V) de cada key (K) son agregados
    dada la funcion f, que deberia de ser de tipo (V, V) => V
    '''
    s = {}
    for e in l:
        key, value = e
        if key not in s:
            s[key] = []
        s[key].append(value)
    out = []
    for key in s.keys():
        out.append((key, reduce(f, s[key])))
    return out
