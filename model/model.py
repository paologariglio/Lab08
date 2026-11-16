from operator import attrgetter

from database import distributore_DAO
from database.distributore_DAO import DistributoreDAO

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._distributori = None
        self.load_distributori()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_distributori(self):
        """ Carica tutti i distributori e li setta nella variabile self._distributori """
        self._distributori = DistributoreDAO.get_distributori()

    def get_prezzo_medio(self, mese:int):
        """
        Calcola, per ogni distributore, il prezzo medio al litro per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome del distributore, media), es. (Distributore A, 1.789)
        """
        # TODO
        risultati = []
        for distributore in self._distributori:
            prezzo = distributore.get_prezzi()
            somma = 0
            contatore = 0
            for p in prezzo:
                if p.data.month == mese:
                    somma += p.prezzo_litro
                    contatore += 1
            if contatore>0:
                media = somma / contatore
                risultati.append((distributore.nome, media))
        return risultati


    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di rifornimenti nei primi 7 giorni
        :return: sequenza di nomi distributore ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        prezzi_settimana = self.__get_prezzi_prima_settimana_mese(mese)

        self.__ricorsione([], 1, None, 0, prezzi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {distributore.id: distributore.nome for distributore in self._distributori}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, round(self.__costo_ottimo, 2)

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_distributore, costo_corrente, prezzi_settimana):
        """ Implementa la ricorsione """
        # TODO
        if giorno>7:
            if self.__costo_ottimo == -1 or costo_corrente < self.__costo_ottimo:
                self.__costo_ottimo = costo_corrente
                self.__sequenza_ottima = list(sequenza_parziale)
            return

        for id_distributore in prezzi_settimana.keys():
            prezzo_oggi = prezzi_settimana[id_distributore][giorno -1]
            costo_benzina = prezzo_oggi * 100
            costo_tassa = 0
            if ultimo_distributore is not None:
                if ultimo_distributore != id_distributore:
                    costo_tassa = 5

            sequenza_parziale.append(id_distributore)

            self.__ricorsione(sequenza_parziale, giorno+1, id_distributore, costo_corrente+costo_benzina+costo_tassa, prezzi_settimana)
            sequenza_parziale.pop()


    def __get_prezzi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i prezzi dei primi 7 giorni del mese selezionato per ciascun distributore.
        :return: un dizionario: {id_distributore: [prezzo_giorno1, ..., prezzo_giorno7]}
        """
        # TODO
        dizionario = { }
        for distributore in self._distributori:
            prezzo = distributore.get_prezzi()


            prezzi_filtrati = [p for p in prezzo if p.data.month == mese and 1<=p.data.day<=7]
            prezzi_filtrati.sort(key=attrgetter("data.day"))

            dizionario[distributore.id] = [p.prezzo_litro for p in prezzi_filtrati]

        return dizionario