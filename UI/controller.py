import flet as ft
from modello.model import Model
from UI.view import View
import time
class Controller:
    def __init__(self, view:View, model:Model):
        # the view, with the graphical elements of the UI
        self._verticePartenza = None
        self._view = view
        # the modello, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listColor = []

    def fillDD(self):
        self._listYear=self._model.Anni
        self._listColor=self._model.Colori
        for colore in self._listColor:
            self._view._ddcolor.options.append(ft.dropdown.Option(key=colore[0],text=colore[0]))
        for anno in self._listYear:
            self._view._ddyear.options.append(ft.dropdown.Option(key=anno[0],text=anno[0]))
        self._view.update_page()


    def handle_graph(self, e):
        if self._view._ddyear.value is None:
            self._view.create_alert("Non hai inserito l'anno")
            self._view.update_page()
            return
        if self._view._ddcolor.value is None:
            self._view.create_alert("Non hai inserito il colore")
            self._view.update_page()
            return

        # Clear dei risultati precedenti
        self._view.txtOut.controls.clear()
        self._model.__init__()

        # Set dei valori scelti
        self._coloreScelto = self._view._ddcolor.value
        self._annoScelto = self._view._ddyear.value



        # Creazione del grafo
        self.grafo=self._model.creaGrafo(self._coloreScelto, self._annoScelto)

        # Aggiornamento dei risultati nella vista
        self._view.txtOut.controls.append(ft.Text("Grafo creato correttamente"))
        self._view.txtOut.controls.append(ft.Text(f"Numero di nodi è :{self._model.numNodes()} Numero di archi è :{self._model.numEdges()}"))
        self._view.txtOut.controls.append(ft.Text("I tre archi con peso maggiore", color="red"))

        # Calcolo delle statistiche e aggiornamento della vista
        lista = self._model.calcolaStatistiche()
        for elemento in lista:
            self._view.txtOut.controls.append(
                ft.Text(f"Arco da {elemento[0].Product_number} a {elemento[1].Product_number},  PESO= {elemento[2]['weight']}"))
        ripetuti = self._model.calcoloMaggiore(lista)

        if len(ripetuti)==0:
            self._view.txtOut.controls.append(ft.Text(f"Nessun codice"))
        else:
            self._view.txtOut.controls.append(ft.Text(f"I codici ripetuti sono: {ripetuti}"))
        # for elemento in ripetuti:
        #     self._view.txtOut.controls.append(ft.Text(elemento))

        # Abilitazione dei controlli
        self._view._ddnode.disabled = False
        self._view.btn_search.disabled = False
        self.fillDDProduct()

        # Aggiornamento della pagina
        self._view.update_page()

    def fillDDProduct(self):
        print(self._model.getProdotti(self._view._ddcolor.value))
        for prodotto in self._model.getProdotti(self._view._ddcolor.value):
            self._view._ddnode.options.append(ft.dropdown.Option(key=prodotto.Product_number, text=prodotto.Product_number,data=prodotto,on_click=self.handleProdotto))
        self._view.update_page()

    def handleProdotto(self,e):
        if e.control.data is None:
            self._verticePartenza=None
        else:
            self._verticePartenza=e.control.data

    def handle_search(self, e):
        self._view.txtOut2.controls.clear()
        if self._view._ddnode is None:
            self._view.create_alert("Non hai inserito il prodotto")
            self._view.update_page()
            return
        start_time = time.time()
        migliore=self._model.cercaPercorso(self._verticePartenza)
        end_time=time.time()
        if len(migliore)==0:
            self._view.txtOut2.controls.append(ft.Text(f"Il percorso migliore ha 0 archi"))
            self._view.update_page()
            return
        self._view.txtOut2.controls.append(ft.Text(f"Il percorso migliore ha {len(migliore)-1} archi"))
        self._view.txtOut2.controls.append(ft.Text(f"Il tempo impiegato è {end_time-start_time} "))
        for elemento in migliore:
            print(elemento)
        self._view.update_page()


