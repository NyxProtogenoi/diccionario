#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#  diccionario.py
#  
#  Copyright 2016  <nyx@kanes>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

from gi.repository import Gtk
import os.path
import re

class VenPrincipal(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self)
		self.set_size_request(400,200)
		self.set_border_width(10)
		
		hb = Gtk.HeaderBar()
		hb.set_show_close_button(True)
		hb.props.title = "Diccionario Nëme v1.0"
		self.set_titlebar(hb)
		
		#Main container
		self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=6)
		self.add(self.box)
		
			
		pestanias = Gtk.Stack()
		pestanias.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
		pestanias.set_transition_duration(500)
		
		
		
########################################################		
#PESTAÑA 1: MANIPULACIÓN DE ENTRADAS / DATA MANIPULATION
########################################################
		visual = Gtk.Box(spacing=6)
		visual.set_border_width(10)
		
		n_vis = "Manipulación de entradas"
		pestanias.add_titled(visual,"Visualizador",n_vis)
		
		
			#===========================================================
			#LISTA DE PALABRAS/WORD LIST--------------------------------
			#===========================================================
		scroll = Gtk.ScrolledWindow()
		visual.pack_start(scroll,True,True,0)
		
				#0.CREACIÓN DE LA STORE/STORE CREATION
		palabras = Gtk.ListStore(str,str)
		
				#1.CONFIRMACIÓN DE EXISTENCIA DE BD/BD EXISTENCE CONFIRMATION
		archivo = "svorste_bd.txt"
		try:
			fuente = open(archivo)
			print "La base de datos existe."
			#fuente.close()						#DEBUG
			#print "Se cerró la base de datos."	#DEBUG
		except:
			print "No existe tal archivo, por lo que se procede a crearlo."
			fuente = open(archivo,"w")
			#fuente.close()						#DEBUG
			#print "Se cerró la base de datos."	#DEBUG
			
		
		fuente = open(archivo)
				#2.OBTENCIÓN LISTA DE PARES/PAIR OBTAINMENT
		svo_espa = []
		for renglon in fuente:
			coordenada = int()
			#print renglon				#DEBUG
			count = 0
			for caracter in renglon:
				if caracter == "|":
					#print count		#DEBUG
					coordenada = renglon.index(caracter)
					#print coordenada	#DEBUG
				count += 1
					#obtención término en Svörste/Svörste termn obtainment:
			en_svorste = renglon[:coordenada]
					#obtención término en Español/Spanish termn obtainment:
			if renglon[-1] == "\n":
				en_espa = renglon[coordenada+1:renglon.index("\n")]
			else:
				en_espa = renglon[coordenada+1:]
					#obtención par Svörste-Español acorde al formato str-str
					#del store/svörste-spanish pair obtainment in store's str-str
					#format:
			s_e = (en_svorste,en_espa)
			svo_espa.append(s_e)
		
		print "Instancia 1: %s" %(svo_espa)

		#for elements in svo_espa:	#DEBUG
		#	print elements			#DEBUG
		
		count = 0
		for par in svo_espa:
			palabras.append(par)
			print par
			print palabras[count]
			count += 1
		
		print "Modelo creado exitosamente."
		
				#3.VISUALIZADOR/DISPLAY
					#3.1 LISTADO/LISTING
		COLUMNAS = ("Svörste","Español")
		visualizador = Gtk.TreeView(model=palabras)

		for elemento in COLUMNAS:
			indice = COLUMNAS.index(elemento)
			#print "índice para agregar columnas: %s" %indice	#DEBUG
			celda = Gtk.CellRendererText()
			col = Gtk.TreeViewColumn(COLUMNAS[indice],celda,text=indice)
						#ésto permite que se ordene alfabéticamente la
						#columna que quiera/this piece of code allows
						#the user to get and alphabetically ordered column
						#just by clicking on the top row:
			visualizador.append_column(col)
			col.set_sort_column_id(indice)
		
					#3.2 FILTRO/FILTER
		filtro = palabras.filter_new()
		
		
					
			#===========================================================
			#OPCIONES/OPTIONS-------------------------------------------
			#===========================================================
		vista_byo = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=6)
		visual.pack_start(vista_byo,False,True,0)	#False clave para que
													#el tamaño del scroll
													#se arregle correctamente
		
				#Entry de búsqueda/Search Entry
		busqueda = Gtk.Entry()
		busqueda.set_placeholder_text("Palabra a buscar.")
		busqueda.connect("changed",self.filtrado,filtro)
		vista_byo.pack_start(busqueda,True,True,0)
				
				#Buscar en Svörste o Español?/Language filter
		idioma = Gtk.Box(spacing=6)
		vista_byo.pack_start(idioma,True,True,0)
		
		self.svorste = Gtk.RadioButton.new_with_label_from_widget(None,"Svörste")
		self.svorste.connect("toggled",self.filtrado,filtro)
		idioma.pack_start(self.svorste,False,False,0)
		
		self.espaniol = Gtk.RadioButton.new_from_widget(self.svorste)
		self.espaniol.set_label("Español")
		self.espaniol.connect("toggled",self.filtrado,filtro)
		idioma.pack_start(self.espaniol,False,False,0)
		
		filtro.set_visible_func(self.filtrar,busqueda)
		
		self.treeview = Gtk.TreeView(model=filtro)
		
		celda1 = Gtk.CellRendererText()
		#print "celda1: %s" %celda1	#DEBUG
		col1 = Gtk.TreeViewColumn("Svörste",celda1,text=0)
		self.treeview.append_column(col1)
		col1.set_sort_column_id(0)
		
		celda2 = Gtk.CellRendererText()
		col2 = Gtk.TreeViewColumn("Español",celda2,text=1)
		self.treeview.append_column(col2)
		col2.set_sort_column_id(1)
		
		scroll.add(self.treeview)	#si no lo muestro, puedo sortear/if I don't add it, I cannot alphabetically sort the column
									#si los muestro a los dos, no sortea/if I show both, I cannot still sort it
		#scroll.add(visualizador)	#si no lo muestro, puedo filtrar/if I show it, I can sort it, but I cannot filter.
		
				#Agregar palabra/Add word
		agregar = Gtk.Button.new_with_label("Agregar")
		agregar.connect("clicked",self.agregar_clickeado,fuente,archivo,palabras,svo_espa,visualizador)
		vista_byo.pack_start(agregar,True,True,0)
		
				#Modificar palabra/Modify word
		modificar = Gtk.Button.new_with_label("Modificar")
		modificar.connect("clicked",self.modificar_clickeado,svo_espa,palabras,VenPrincipal,svo_espa,fuente,archivo,visualizador)
		vista_byo.pack_start(modificar,True,True,0)
		
				#Eliminar palabra/Delete word
		eliminar = Gtk.Button.new_with_label("Eliminar")
		eliminar.connect("clicked",self.eliminar_clickeado,palabras,svo_espa,fuente,archivo,visualizador)
		vista_byo.pack_start(eliminar,True,True,0)
		
################################################
#PESTAÑA 2: CONJUGADOR DE VERBOS/VERB CONJUGATOR
################################################
		self.conjugador = Gtk.Box(spacing=6)
		self.conjugador.set_border_width(2)

		n_verb = "Conjugador de verbos"
		pestanias.add_titled(self.conjugador,"Visualizador",n_verb)
		
		#Lista con verbos/Verb list
		scroll_conj = Gtk.ScrolledWindow()
		scroll_conj.set_size_request(200,400)
		self.conjugador.pack_start(scroll_conj,True,True,0)
		
		conjugar = Gtk.ListStore(str,str)
		se_conj = list()
		
		for par in svo_espa:
			if par[1][-2:] == ("ar" or "er" or "ir"):
				se_conj.append(par)
		
		#print "Palabras en se_conj: %s" %se_conj	#DEBUG
		
		for par in se_conj:
			conjugar.append(par)
		
		#print "Fertig"	#DEBUG
		
		conjugator = Gtk.TreeView(model=conjugar)

		for elemento in COLUMNAS:
			indice = COLUMNAS.index(elemento)
			print "índice para agregar colucnas: %s" %indice
			celda = Gtk.CellRendererText()
			col = Gtk.TreeViewColumn(COLUMNAS[indice],celda,text=indice)
			conjugator.append_column(col)
			col.set_sort_column_id(indice)
			
		scroll_conj.add(conjugator)
		
		#Conjugación del verbo seleccionado/Chosen verb conjugation
		self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=6)
		self.conjugador.pack_start(self.vbox,True,False,0)
		
		clickeado = conjugator.get_selection()
		clickeado.connect("changed",self.conjugando)
		
		conjugaciones_presente = (
			("Presente I","í"),
			("Futuro I","á"),
			("Pretérito Perfecto Simple","ó"),
			("Pretérito Imperfecto I","é"),
			("Condicional","ái"))
		conjugaciones_subjuntivo = (
			("Presente","ís"),
			("Pretérito Imperfecto","és"),
			("Futuro","ás"))
		conjugaciones_restantes = (
			("Imperativo","ít"),
			("Gerundio","ú"),
			("Participio Pasivo","ót"))
			
		self.conjugaciones = (conjugaciones_presente,conjugaciones_subjuntivo,conjugaciones_restantes)
		self.modos = ("Indicativo","Subjuntivo","Otras conjugaciones")
		
		self.entries = list()
		
		count = 0
		for elemento in self.conjugaciones:
			#print "Elemento:"	#DEBUG
			#print elemento		#DEBUG
			label = Gtk.Label()
			if count != 2:
				lab_mark = "Modo " + self.modos[count]
			else:
				lab_mark = self.modos[count]
			label.set_markup(lab_mark)
			#print "QUIERES CAMBIAR MIS MODOS: %s" %self.modos[count]	#DEBUG
			self.vbox.pack_start(label,True,True,0)
				
			count_1 = 0
			for par in self.conjugaciones[count]:
				time_box = Gtk.Box(spacing=2)
				#print "Paar:"	#DEBUG
				#print par		#DEBUG
				label_1 = Gtk.Label()
				lab = self.conjugaciones[count][count_1][0]
				#print lab		#DEBUG
				label_1.set_markup(lab)
				label_1.set_xalign(0)
				
				self.entry_1 = Gtk.Entry()
				self.entry_1.set_name(lab)
				self.entry_1.set_editable(False)
				
				pares = (self.entry_1,lab)
				
				self.entries.append(pares)
				
				time_box.pack_start(label_1,True,True,0)
				time_box.pack_start(self.entry_1,True,True,0)
				
				self.vbox.pack_start(time_box,True,True,0)
				self.vbox.set_homogeneous(True)
				
				count_1 += 1
			count += 1
		
		#print "This is it %s" %self.entries	#DEBUG
		

###############
#STACK-SWITCHER
###############
		switcher = Gtk.StackSwitcher()
		switcher.set_stack(pestanias)
		self.box.pack_start(switcher,True,True,0)
		self.box.pack_start(pestanias,True,True,0)
		
####################
#FUNCIONES/FUNCTIONS
####################
	
	def agregar_clickeado(self,button,fuente,archivo,palabras,svo_espa,visualizador):
		#print "Agregáu"	#DEBUG
		
		class Agregar(Gtk.Window):
			def __init__(self):
				Gtk.Window.__init__(self,title="Agregar palabra nueva")
				
				self.set_border_width(10)
				
				vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=6)
				self.add(vbox)
				
				s_et = Gtk.Label()
				s_et.set_label("Svörste: ")
				vbox.pack_start(s_et,True,True,0)
				svorste = Gtk.Entry()
				vbox.pack_start(svorste,True,True,0)
				
				e_et = Gtk.Label()
				e_et.set_label("Español: ")
				vbox.pack_start(e_et,True,True,0)
				espaniol = Gtk.Entry()
				vbox.pack_start(espaniol,True,True,0)
				
				hbox = Gtk.Box(spacing=6)
				vbox.pack_start(hbox,True,True,0)
				
				cancelar = Gtk.Button.new_with_label("Cancelar")
				cancelar.connect("clicked",self.cerrar)
				hbox.pack_start(cancelar,True,True,0)
					
				aceptar = Gtk.Button.new_with_label("Aceptar")
				aceptar.connect("clicked",self.aceptar,fuente,archivo,espaniol,svorste,palabras,svo_espa,visualizador)
				hbox.pack_start(aceptar,True,True,0)
					
				vbox.show_all()
				
			def cerrar(self,button):
				Agregar.destroy(self)
			
			def aceptar(self,widget,fuente,archivo,espaniol,svorste,palabras,svo_espa,visualizador):
				s_e_0 = svorste.get_text()
				s_e_1 = espaniol.get_text()
				#print s_e_0	#DEBUG
				#print s_e_1	#DEBUG
				se_01 = (s_e_0,s_e_1)
				
				svo_espa.append(se_01)
				
				palabras.clear()
				for par in svo_espa:
					palabras.append(par)
				#print "Alles gut!"	#DEBUG
				#print svo_espa		#DEBUG
				
				fuente.close()
				fuente = open(archivo,"a")
				#print espaniol.get_text()	#DEBUG
				for par in svo_espa:
					if par == svo_espa[0]:
						par_nuevo = svorste.get_text() + "|" + espaniol.get_text()
					else:
						par_nuevo = "\n" + svorste.get_text() + "|" + espaniol.get_text()
				#print par_nuevo	#DEBUG
				fuente.write(par_nuevo)
				#print "Base de datos actualizada correctamente."	#DEBUG
				espaniol.set_text("")
				svorste.set_text("")
				fuente.close()
				
				espaniol.set_text("")
				svorste.set_text("")
				
				visualizador = Gtk.TreeView(model=palabras)
				visualizador.show_all()
				
				
		ven = Agregar()
		ven.connect("delete-event",Gtk.main_quit)
		ven.show_all()
		Gtk.main()
				
			
	
	def modificar_clickeado(self,button,pares,palabras,VenPrincipal,svo_espa,fuente,archivo,visualizador):
		#print "Modificáu"	#DEBUG
		class Modificar(Gtk.Window):
			def __init__(self):
				Gtk.Window.__init__(self,title="Modificar palabra existente")
				
				self.set_border_width(10)
				
				vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=6)
				self.add(vbox)
				
				sprache = Gtk.Box(spacing=6)
				vbox.pack_start(sprache,True,True,0)
				
				svorste = Gtk.RadioButton.new_with_label_from_widget(None,"Svörste")
				svorste.connect("toggled",self.sprache,"1",vbox,pares,palabras,VenPrincipal,svo_espa,fuente,archivo,visualizador)
				sprache.pack_start(svorste,False,False,0)
				
				espaniol = Gtk.RadioButton.new_from_widget(svorste)
				espaniol.set_label("Español")
				espaniol.connect("toggled",self.sprache,"2",vbox,pares,palabras,VenPrincipal,svo_espa,fuente,archivo,visualizador)
				sprache.pack_start(espaniol,False,False,0)
				
			
			def sprache(self,button,name,vbox,pares,palabras,VenPrincipal,svo_espa,fuente,archivo,visualizador):
				if button.get_active():
					state = "on"
					print "Búsqueda configurada para %s" %(name)
					
					etiqueta = button.get_label()
					
					idioma = Gtk.Label(etiqueta)
					vbox.pack_start(idioma,True,True,0)
						#LISTA DESPLEGABLE DE TERMINOS A MODIFICAR/Terms available for modification dropdown list
					combo = Gtk.ComboBoxText()
					count = 0
					if etiqueta == "Svörste":
						for elemento in pares:
							combo.insert(count,str(count),str(pares[count][0]))
							count += 1
					else:
						for elemento in pares:
							combo.insert(count,str(count),str(pares[count][1]))
							count += 1
					vbox.pack_start(combo,False,True,0)
					
					modificacion = Gtk.Entry()
					modificacion.set_placeholder_text("Nueva expresión.")
					vbox.pack_start(modificacion,True,True,0)
					
					hbox = Gtk.Box(spacing=6)
					vbox.pack_start(hbox,True,True,0)
					
					cancelar = Gtk.Button.new_with_label("Cancelar")
					cancelar.connect("clicked",self.cerrar)
					hbox.pack_start(cancelar,True,True,0)
					
					aceptar = Gtk.Button.new_with_label("Aceptar")
					aceptar.connect("clicked",self.aceptar,combo,modificacion,etiqueta,palabras,VenPrincipal,svo_espa,fuente,archivo,visualizador)
					hbox.pack_start(aceptar,True,True,0)
					
					vbox.show_all()
				else:
					state = "off"
					
			def cerrar(self,button):
				Modificar.destroy(self)	
			
			def aceptar(self,button,combo,modificacion,etiqueta,palabras,VenPrincipal,svo_espa,fuente,archivo,visualizador):
				#print etiqueta		#DEBUG
				name = combo.get_active_text()
				#print name			#DEBUG
				nuevo = modificacion.get_text()
				#print nuevo		#DEBUG
				count = 0
				for par in svo_espa:
					#print par		#DEBUG
					if etiqueta == "Svörste":
						if svo_espa[count][0] == name:
							svo_espa[count][0] == nuevo
							#print "Está saliendo bien."	#DEBUG
					elif etiqueta == "Español":
						if svo_espa[count][1] == name:
							neu_par_0 = par[0]
							neu_par = (neu_par_0,nuevo)
							#print count					#DEBUG
							del svo_espa[count]
							svo_espa.append(neu_par)
							#print neu_par					#DEBUG
							#print svo_espa					#DEBUG
							#print "En Spagnolo é tuto bene!"	#DEBUG
							
					count += 1
				palabras.clear()
				for par in svo_espa:
					palabras.append(par)
				#print "Alles gut!"	#DEBUG
				
				fuente.close()
				fuente = open(archivo,"w")
				for par in svo_espa:
					if par == svo_espa[0]:
						par_nuevo = par[0] + "|" + par[1]
					else:
						par_nuevo = "\n" + par[0] + "|" + par[1]
					#print par_nuevo	#DEBUG
					fuente.write(par_nuevo)
				#print "Base de datos reescrita excitosamente."	#DEBUG
				
				modificacion.set_text("")
				
				visualizador = Gtk.TreeView(model=palabras)
				visualizador.show_all()
				
		ven = Modificar()
		ven.connect("delete-event",Gtk.main_quit)
		ven.show_all()
		Gtk.main()		
			
		
	def eliminar_clickeado(self,button,palabras,svo_espa,fuente,archivo,visualizador):
		#print "Elimináu"	#DEBUG
		seleccion = self.treeview.get_selection() #ahora lo que se ve es self.treeview
		#print "selección: %s" %seleccion	#DEBUG
		(modelo,pathlist) = seleccion.get_selected_rows()
		#print "modelo: %s" %modelo	#DEBUG
		#print "pathlist: %s" %pathlist	#DEBUG
		
		v_se = []
		for path in pathlist:
			tree_iter = modelo.get_iter(path)
			#print tree_iter	#DEBUG
			value = modelo.get_value(tree_iter,0)
			value_1 = modelo.get_value(tree_iter,1)
			v_se = (value,value_1)
		#print v_se	#DEBUG
		count = 0
		for elemento in svo_espa:
			if elemento == v_se:
				del svo_espa[svo_espa.index(elemento)]
		#print svo_espa			#DEBUG
		#print "Está hecho."		#DEBUG
		#print v_se[0]				#DEBUG
		#print v_se[1]			#DEBUG
		
		#se vacía la ListStore/ListStore is emptied
		palabras.clear()
		
		#se la vuelve a llenar con la lista de palabras modificada/and now
		#refilled with the new modified word list:
		for par in svo_espa:
			palabras.append(par)
		#print "Alles klar!"		#DEBUG
		
		
		#se modifica la lista que ve el usuario/the list displayed is
		#also refreshed
		visualizador = Gtk.TreeView(model=palabras)
		visualizador.show_all()
		
		#se modifica a su vez la Base de Datos/DB also modified
		fuente.close()
		fuente = open(archivo,"w")
		for par in svo_espa:
			if par == svo_espa[0]:
				par_nuevo = par[0] + "|" + par[1]
			else:
				par_nuevo = "\n" + par[0] + "|" + par[1]
			#print par_nuevo		#DEBUG
			fuente.write(par_nuevo)
		#print "Base de datos reescrita excitosamente."		#DEBUG
		
	
	def filtrar(self,visualizador,iter,busqueda,data=None):
		buscador = busqueda.get_text()
		svo = self.svorste.get_active()
		esp = self.espaniol.get_active()
		
		buscar_todas_columnas_s = svo == 0
		buscar_todas_columnas_e = esp == 1
		
		if buscador == "":
			return True
			
		if buscar_todas_columnas_s and buscar_todas_columnas_e:
			for col in range(1,self.treeview.get_n_columns()):
				value = visualizador.get_value(iter,col)
				if value.startswith(buscador):
					return True
			return False
		
		if svo == 1 and esp == 0:
			value = visualizador.get_value(iter,esp)
		elif esp == 1 and svo == 0:
			value = visualizador.get_value(iter,svo)
		return True if value.startswith(buscador) else False
		
		#print "svo: %s" %svo		#DEBUG
		#print "esp: %s" %esp		#DEBUG
		
	def filtrado(self,widget,filtro):
		filtro.refilter()
		
	def conjugando(self,seleccion):
		clickeado = seleccion
		(mod,pathl) = clickeado.get_selected_rows()
		
			#Obtención del verbo a conjugar en función de la línea seleccionada/
			#Verb to conjugate obtainment in relation to the selected row
		v_a_conjugar = []
		for path in pathl:
			conj_iter = mod.get_iter(pathl)
			print "conj_iter %s" %conj_iter
			v_a_conjugar = mod.get_value(conj_iter,0)

		raiz = v_a_conjugar[:-1]
		
		#print "CLIQUEADO: %s" %clickeado	#DEBUG
		
		if len(v_a_conjugar) == 0:
			#print "NO PASA NARANJA"	#DEBUG
			pass
		
		else:
			markups = list()		
			count = 0
			for elemento in self.conjugaciones:
				#print "Elementos dentro de la lista de conjugación:"	#DEBUG
				#print elemento		#DEBUG
				
				count_1 = 0
				for par in self.conjugaciones[count]:
					#print "par del conjugaciones:" 	#DEBUG
					#print par		#DEBUG
					markup_entry = raiz + "-" + self.conjugaciones[count][count_1][1]
					#print "markup_entry: %s" %markup_entry		#DEBUG
					
					count_2 = 0
					for elementos in self.entries:
						#print "elemento del self.entries:" 	#DEBUG
						#print elementos		#DEBUG
						if elementos[1] == par[0]:
							#print "ALGO PASA"	#DEBUG
							#print elementos[1]	#DEBUG
							elementos[count_2].set_text(markup_entry)
						#else:					#DEBUG
						#	print "NO ESTÁ PASANDO NADA"	#DEBUG
					
					markups.append(markup_entry)
									
					count_1 += 1
				count += 1

			
ventana = VenPrincipal()
ventana.connect("delete-event",Gtk.main_quit)
ventana.show_all()
Gtk.main()
