import time
import flet as ft
from model.nerc import Nerc


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._mappaNercValue = {}
        self.fillMappaNercValue()


    # -----------------------------------------------------------------------------------------------------------------------------
    def fillDD(self):

        # non serve salvarlo come oggetto, è piu facile farsi una mappa poi dopo
        nercList = self._model.getListNerc()
        for n in nercList:
            self._view._ddNerc.options.append(ft.dropdown.Option(n))
        self._view.update_page()

    # -----------------------------------------------------------------------------------------------------------------------------
    def fillMappaNercValue(self):

        # serve per gestire gli oggetti nerc
        nerc = self._model.getListNerc()
        for v in nerc:
            self._mappaNercValue[v.value] = v

    #-----------------------------------------------------------------------------------------------------------------------------
    def handleWorstCase(self, e):

        self._view._txtOut.controls.clear()

        #errore comune: se dal dropdown fai .value allora prendi una stringa.
        #soluzione: crea una mappa in cui hai chiave: str value, valore: ogg Nerc

        nerc_value = self._view._ddNerc.value
        nerc = self._mappaNercValue.get(nerc_value)

        anni= self._view._txtYears.value
        ore= self._view._txtHours.value

        start = time.time()

        if nerc is None:
            self._view.create_alert("Inserire un NERC!")
        if anni is None:
            self._view.create_alert("Inserire un anno!")
        if ore is None:
            self._view.create_alert("Inserire un anno!")

        solBest, utentiMax, oreBest = self._model.getWorstCase(nerc, anni, ore)
        end = time.time()

        self._view._txtOut.controls.append( ft.Text( f"People affected: {utentiMax}"))
        self._view._txtOut.controls.append(ft.Text(f"Hours of outage: {oreBest}"))
        for evento in solBest:
            self._view._txtOut.controls.append( ft.Text( evento.__str__() ) )
        self._view._txtOut.controls.append( ft.Text( f"Elapsed time: {end-start}"))

        self._view.update_page()



