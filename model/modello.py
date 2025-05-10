import copy

from database.DAO import DAO
from model.nerc import Nerc
from model.powerOutages import Event


class Model:
    def __init__(self):
        self._solBest = []
        self._listNerc = None
        self._listEventsNerc = None
        self._utentiMax = 0
        self._oreBest = 0
        #self.loadNerc()

    # -----------------------------------------------------------------------------------------------------------------------------
    def getWorstCase(self, nerc, anni, ore):

        self._listEventsNerc = DAO.getAllEvents(nerc)
        self._solBest = []
        self._utentiMax = 0
        self._oreBest = 0

        self.ricorsione([], 0, anni, ore, self._listEventsNerc)
        ore_disservizio = self.calcolaOreDisservizio(self._solBest)

        return self._solBest, self._utentiMax, self._oreBest
        
    # -------------------------------------------------------------------------------------------------------------------------------
    def ricorsione(self, parziale, livello, anni, ore, lista_eventi):

        #condizione terminale
        # len(parziale)==len(lista_eventi)) --> NO: non considera i sottoinsieme, ma solo gli eventi
        # if self.isAmmissibile() --> NO: se il parziale è ammissibile ti fermi, e quindi non aggiungi altri eventi validi

        if livello == len(lista_eventi):  #non ci sono più eventi da aggiungere a partire dal livello attuale
            print(parziale)
            if self.isAmmissibile(parziale, anni, ore):
                utenti_disservizio = self.calcolaUtentiDisservizio(parziale)
                ore_disservizio = self.calcolaOreDisservizio(parziale)

                if utenti_disservizio > self._utentiMax:
                    print("NUOVA SOLUZIONE MIGLIORE!")
                    self._utentiMax = utenti_disservizio
                    self._oreBest = ore_disservizio         #salvo il dato --> inizializzato nel costruttore
                    self._solBest = copy.deepcopy(parziale) #serve perchè al passo successivo perdi parziale come solBest

        else:
            # condizione di ricorsione
            evento_corrente = lista_eventi[livello]
            if evento_corrente not in parziale:
                parziale.append(evento_corrente)
                self.ricorsione(parziale, livello+1, anni, ore, lista_eventi)
                parziale.pop()

    # -----------------------------------------------------------------------------------------------------------------------------
    def isAmmissibile(self, parziale: list[Event],  anni, ore):

        if len(parziale) == 0:
            return True

        #1. indicazione su come calcolare correttamente la durata di un evento.
            # dice di non usare un campo pre-calcolato o approssimativo, ma di calcolare --> durata_evento --> ore_evento

        ore_disservizio = self.calcolaOreDisservizio(parziale)

        #2. ore_disservizio <= ore
        if ore_disservizio > int(ore):
            return False

        #3. differenza anno + recente e anno vecchio <= anni:
        anno_vecchio = min( evento.date_event_began.year for evento in parziale)
        anno_recente = max( evento.date_event_finished.year for evento in parziale)
        if (anno_recente - anno_vecchio) > int(anni):
            return False

        return True

    # -----------------------------------------------------------------------------------------------------------------------------
    def calcolaOreDisservizio(self, parziale: list[Event] ): #solBest

        oreDisservizio = 0
        for evento in parziale:
            durata = evento.date_event_finished - evento.date_event_began
            durataOre = durata.total_seconds() / 3600   #total_seconds() --> funzione di python
            oreDisservizio += durataOre
        return oreDisservizio

    # -----------------------------------------------------------------------------------------------------------------------------
    def calcolaUtentiDisservizio(self, parziale: list[Event]):

        numUtenti = 0
        for evento in parziale:
            numUtenti += evento.customers_affected
        return numUtenti

    # -----------------------------------------------------------------------------------------------------------------------------
    def calcolaAnnoMin(self, parziale):

        annoMin = 10000000
        for evento in parziale:
            if evento.date_event_began.year < annoMin:
                annoMin = evento.date_event_began.year
        return annoMin

    # -----------------------------------------------------------------------------------------------------------------------------
    def calcolaAnnoMax(self, parziale):

        annoMax = 0
        for evento in parziale:
            if evento.date_event_finished.year > annoMax:
                annoMax = evento.date_event_finished.year
        return annoMax

    # -----------------------------------------------------------------------------------------------------------------------------

    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)

    def getListNerc(self):
        return DAO.getAllNerc()

    # -----------------------------------------------------------------------------------------------------------------------------
    @property
    def listNerc(self):
        return self._listNerc


# -----------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    model = Model()
    nerc = Nerc(1, "ERCOT")
    listaEventiNerc = DAO.getAllEvents(nerc)
    print(listaEventiNerc)

    lista_eventi, utenti, oreDisservizio = model.getWorstCase(nerc, 4, 200)
    for evento in lista_eventi:
        print(evento)
    print(f'utenti disservizio {utenti}')
    print(f'ore disservizio {oreDisservizio}')
