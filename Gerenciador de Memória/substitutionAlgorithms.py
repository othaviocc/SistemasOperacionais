from copy import copy

class Fifo:
    @staticmethod
    def substitute_page_local(**kwargs):
        kwargs['pages'].pop(0)
        kwargs['pages'].append(kwargs['new_page'])
        return kwargs['pages']
    
    @staticmethod
    def increment_counter(counter, page):
        pass

class MRU:
    @staticmethod
    def substitute_page_local(**kwargs):
        counter_pages = dict(map(lambda x: (x,kwargs['counter'][x]), kwargs['pages'])) # Filtra o dicionário para mostrar apenas os valores que estão na moldura
        kwargs['pages'].remove(max(counter_pages, key=counter_pages.get)) # Remove das paginas a chave cujo valor é maior
        kwargs['pages'].append(kwargs['new_page'])
        return kwargs['pages']
    
    @staticmethod
    def increment_counter(counter, page):
        for c in counter:
            counter[c] += 1
        counter[page] = 0
        return counter

class NUF:
    @staticmethod
    def substitute_page_local(**kwargs):
        counter_pages = dict(map(lambda x: (x,kwargs['counter'][x]), kwargs['pages'])) # Filtra o dicionário para mostrar apenas os valores que estão na moldura
        min_value = (min(counter_pages.values())) # Seleciona o menor valor das chaves
        page_to_remove = min([k for k, v in counter_pages.items() if v == min_value]) # De todas as chaves com valor mínimo, seleciona-se a menor delas
        kwargs['pages'].remove(page_to_remove)
        kwargs['pages'].append(kwargs['new_page'])
        return kwargs['pages']
    
    @staticmethod
    def increment_counter(counter, page):
        counter[page] = counter.get(page, 0) + 1
        return counter

class Otimo:
    @staticmethod
    def substitute_page_local(**kwargs):
        used_pages = copy(kwargs['pages'])
        for p in kwargs['sequence']:
            if len(used_pages) == 1: # Se achou a última página a ser trocada
                break
            elif p in used_pages:
                used_pages.remove(p)
        kwargs['pages'].remove(used_pages[0]) # Caso existam páginas que não serão mais utilizadas o laço será quebrado sozinho
        kwargs['pages'].append(kwargs['new_page'])
        return kwargs['pages']

    @staticmethod
    def increment_counter(counter, page):
        pass