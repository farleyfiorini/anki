# -*- coding: utf-8 -*-
#
# Para adicionar o Gabarito antes e depois da resposta
# Edited version made by Remco32
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
# Version: 1.0, 2016/03/13

import os
from anki.hooks import addHook
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QIcon, QAction
from anki.hooks import wrap
from aqt.editor import Editor
from anki.utils import json
from BeautifulSoup import BeautifulSoup
from aqt import mw
from aqt.utils import showInfo
from aqt import browser



def comparaInicio(strPrincipal, strSecundaria):
    '''Compara duas Strings retornando verdadeiro
    se o inicio da strPrincipal coincidir com
    a strSecundaria.
    '''
    print("Iniciando Funcao comparaInicio(",strPrincipal,",",strSecundaria,")...")
    
    if len(strPrincipal) < len(strSecundaria):
        print ("strPrincipal < strSecundaria")
        print ("return False\n")
        return False
    else:
        print ("strPrincipal >= strSecundaria...")
        print ("Comparando o inicio da strPrincipal com a strSecundaria...")
        
        if strPrincipal[0:len(strSecundaria)] == strSecundaria:
            print (strPrincipal[0:len(strSecundaria)],"==",strSecundaria)
            print ("return True\n")
            
            return True
        else:
            print (strPrincipal[0:len(strSecundaria)],"!=",strSecundaria)
            print ("return False\n")
            
            return False

def comparaFinal(strPrincipal, strSecundaria):
    '''Compara duas Strings retornando verdadeiro
    se o final da strPrincipal coincidir com
    a strSecundaria.
    '''
    print("Iniciando Funcao comparaFinal(",strPrincipal,",",strSecundaria,")...")
    
    if len(strPrincipal) < len(strSecundaria):
        print ("strPrincipal < strSecundaria")
        print ("return False\n")
        return False
    else:
        print ("strPrincipal >= strSecundaria...")
        print ("Comparando o final da strPrincipal com a strSecundaria...")
        
        if strPrincipal[len(strPrincipal)-len(strSecundaria):len(strPrincipal)] == strSecundaria:
            print (strPrincipal[len(strPrincipal)-len(strSecundaria):len(strPrincipal)],"==",strSecundaria)
            print ("return True\n")
            
            return True
        else:
            print (strPrincipal[len(strPrincipal)-len(strSecundaria):len(strPrincipal)],"!=",strSecundaria)
            print ("return False\n")
            
            return False
        
def limpaTextoInicio (strPrincipal,strSecundaria):
    print("Iniciando funcao limpaTextoInicio(",strPrincipal,",",strSecundaria,")...")
    print("Comparando Strings...")
    if comparaInicio (strPrincipal.lower(),strSecundaria.lower()):
        print("Texto semelhante encontrado...")
        print("return",strPrincipal[len(strSecundaria):len(strPrincipal)])
        return strPrincipal[len(strSecundaria):len(strPrincipal)]
    else:
        print("O texto nao e semelhante...")
        print("return",strPrincipal)
        return strPrincipal

def limpaTextoFinal (strPrincipal,strSecundaria):
    print("Iniciando funcao limpaTextoFinal(",strPrincipal,",",strSecundaria,")...")
    print("Comparando Strings...")
    if comparaFinal (strPrincipal.lower(),strSecundaria.lower()):
        print("Texto semelhante encontrado...")
        print("return",strPrincipal[0:len(strPrincipal)-len(strSecundaria)])
        return strPrincipal[0:len(strPrincipal)-len(strSecundaria)]
    else:
        print("O texto nao e semelhante...")
        print("return",strPrincipal)
        return strPrincipal

def limpaTexto (strPrincipal,strSecundaria):
    strPrincipal = limpaTextoInicio (strPrincipal,strSecundaria)
    strPrincipal = limpaTextoFinal (strPrincipal,strSecundaria)
    
    return strPrincipal

def limpaTextoCerto (str):
    str =str.replace("</br>", "<br>")
    str =str.replace("<br/>", "<br>")
    str =str.replace("<br />", "<br>")
    str =str.replace("</ br>", "<br>")
    str =str.replace(" <br>", "<br>")
    str =str.replace(" <br>", "<br>")
    str =str.replace(" </div><br>", "</div>")
    str =str.replace(" <br><div", "<div")
    str =str.replace("&nbsp;", " ")
    
    str =str.replace('<font color="#0000ff"><b>Correto</b></font>',"Certo")
    str =str.replace('<font color="#0000ff"><b>CORRETO</b></font>',"Certo")
    str =str.replace('<font color="#0000ff"><b>Correta</b></font>',"Certo")
    str =str.replace('<font color="#0000ff"><b>CORRETA</b></font>',"Certo")
    str =str.replace('<font color="#0000ff"><b>Certo</b></font>',"Certo")
    str =str.replace('<font color="#0000ff">Certo</font>',"Certo")    
    str =str.replace('<font color="#0000ff"><b>Certo</b></font>',"Certo")
    str =str.replace('<font color="#0000ff">Certa</font>',"Certo")
    str =str.replace('<font color="#0000ff"><b>CERTO</b></font>',"Certo")
    str =str.replace('<font color="#0000ff">CERTO</font>',"Certo")
    
    str =str.replace("<br><br>Gabarito: Certo","Gabarito: Certo")
    str =str.replace("<br>Gabarito: Certo","Gabarito: Certo")
    
    str = str.replace ("<div>Gabarito: Certo.</div>","")
    str = str.replace ("<div>Gabarito: Certo</div>","")
    str = str.replace ("<div>Gabarito: CERTO.</div>","")
    str = str.replace ("<div>Gabarito: CERTO</div>","")
    str = str.replace ("<div>Gabarito: Certa.</div>","")
    str = str.replace ("<div>Gabarito: Certa</div>","")
    str = str.replace ("<div>Gabarito: CERTA.</div>","")
    str = str.replace ("<div>Gabarito: CERTA</div>","")   
        
    
    str = limpaTexto(str, "Resposta: Certa.")
    str = limpaTexto(str, "Resposta: CERTA.")
    str = limpaTexto(str, "Resposta: Correta.")
    str = limpaTexto(str, "Resposta: Certa!")
    str = limpaTexto(str, "Resposta: CERTA!")
    str = limpaTexto(str, "Resposta: Correta!")
    str = limpaTexto(str, "Resposta: Certa")
    str = limpaTexto(str, "Resposta: CERTA")
    str = limpaTexto(str, "Resposta: Correta")
    str = limpaTexto(str, "Gabarito: Certa.")
    str = limpaTexto(str, "Gabarito: CERTA.")
    str = limpaTexto(str, "Gabarito: Correta.")
    str = limpaTexto(str, "Gabarito: Certa!")
    str = limpaTexto(str, "Gabarito: CERTA!")
    str = limpaTexto(str, "Gabarito: Correta!")
    str = limpaTexto(str, "Gabarito: Certa")
    str = limpaTexto(str, "Gabarito: CERTA")
    str = limpaTexto(str, "Gabarito: Correta")
    
    str = limpaTexto(str, "Resposta: Certo.")
    str = limpaTexto(str, "Resposta: CERTO.")
    str = limpaTexto(str, "Resposta: Correto.")
    str = limpaTexto(str, "Resposta: Certo!")
    str = limpaTexto(str, "Resposta: CERTO!")
    str = limpaTexto(str, "Resposta: Correto!")
    str = limpaTexto(str, "Resposta: Certo")
    str = limpaTexto(str, "Resposta: CERTO")
    str = limpaTexto(str, "Resposta: Correto")
    str = limpaTexto(str, "Gabarito: Certo.")
    str = limpaTexto(str, "Gabarito: CERTO.")
    str = limpaTexto(str, "Gabarito: Correto.")
    str = limpaTexto(str, "Gabarito: Certo!")
    str = limpaTexto(str, "Gabarito: CERTO!")
    str = limpaTexto(str, "Gabarito: Correto!")
    str = limpaTexto(str, "Gabarito: Certo")
    str = limpaTexto(str, "Gabarito: CERTO")
    str = limpaTexto(str, "Gabarito: Correto")
    
    str = limpaTexto(str, "Resposta Certa.")
    str = limpaTexto(str, "Resposta CERTA.")
    str = limpaTexto(str, "Resposta Correta.")
    str = limpaTexto(str, "Resposta Certa!")
    str = limpaTexto(str, "Resposta CERTA!")
    str = limpaTexto(str, "Resposta Correta!")
    str = limpaTexto(str, "Resposta Certa")
    str = limpaTexto(str, "Resposta CERTA")
    str = limpaTexto(str, "Resposta Correta")
    str = limpaTexto(str, "Gabarito Certa.")
    str = limpaTexto(str, "Gabarito CERTA.")
    str = limpaTexto(str, "Gabarito Correta.")
    str = limpaTexto(str, "Gabarito Certa!")
    str = limpaTexto(str, "Gabarito CERTA!")
    str = limpaTexto(str, "Gabarito Correta!")
    str = limpaTexto(str, "Gabarito Certa")
    str = limpaTexto(str, "Gabarito CERTA")
    str = limpaTexto(str, "Gabarito Correta")
    
    str = limpaTexto(str, "Beleza!")
    str = limpaTexto(str, "Perfeito!")
    str = limpaTexto(str, "Exato!")
    str = limpaTexto(str, "Perfeita!")
    str = limpaTexto(str, "Exata!")
    str = limpaTexto(str, "Beleza.")
    str = limpaTexto(str, "Perfeito.")
    str = limpaTexto(str, "Exato.")
    str = limpaTexto(str, "Perfeita.")
    str = limpaTexto(str, "Exata.")
    str = limpaTexto(str, "Certo.")
    str = limpaTexto(str, "CERTO.")
    str = limpaTexto(str, "Certa.")
    str = limpaTexto(str, "CERTA.")
    str = limpaTexto(str, "Certo!")
    str = limpaTexto(str, "CERTO!")
    str = limpaTexto(str, "Certa!")
    str = limpaTexto(str, "CERTA!")
    str = limpaTexto(str, "Certo")
    str = limpaTexto(str, "CERTO")
    str = limpaTexto(str, "Certa")
    str = limpaTexto(str, "CERTA")
    
    str = limpaTexto(str, "Resposta Certo.")
    str = limpaTexto(str, "Resposta CERTO.")
    str = limpaTexto(str, "Resposta Correto.")
    str = limpaTexto(str, "Resposta Certo!")
    str = limpaTexto(str, "Resposta CERTO!")
    str = limpaTexto(str, "Resposta Correto!")
    str = limpaTexto(str, "Resposta Certo")
    str = limpaTexto(str, "Resposta CERTO")
    str = limpaTexto(str, "Resposta Correto")
    str = limpaTexto(str, "Gabarito Certo.")
    str = limpaTexto(str, "Gabarito CERTO.")
    str = limpaTexto(str, "Gabarito Correto.")
    str = limpaTexto(str, "Gabarito Certo!")
    str = limpaTexto(str, "Gabarito CERTO!")
    str = limpaTexto(str, "Gabarito Correto!")
    str = limpaTexto(str, "Gabarito Certo")
    str = limpaTexto(str, "Gabarito CERTO")
    str = limpaTexto(str, "Gabarito Correto")
    
    str = limpaTexto(str, "Certo.")
    str = limpaTexto(str, "Certo!")
    str = limpaTexto(str, "Certo")
    
    str = limpaTexto(str, "Certa.")
    str = limpaTexto(str, "Certa!")
    str = limpaTexto(str, "Certa")

    str = limpaTexto(str, "CERTO.")
    str = limpaTexto(str, "CERTO!")
    str = limpaTexto(str, "CERTO")
    
    str = limpaTexto(str, "CERTA.")
    str = limpaTexto(str, "CERTA!")
    str = limpaTexto(str, "CERTA")
    
    str = limpaTexto(str, "Correto.")
    str = limpaTexto(str, "Correto!")
    str = limpaTexto(str, "Correto")
    
    str = limpaTexto(str, "Correta.")
    str = limpaTexto(str, "Correta!")
    str = limpaTexto(str, "Correta")

    str = limpaTexto(str, "CORRETO.")
    str = limpaTexto(str, "CORRETO!")
    str = limpaTexto(str, "CORRETO")
    
    str = limpaTexto(str, "CORRETA.")
    str = limpaTexto(str, "CORRETA!")
    str = limpaTexto(str, "CORRETA")
    
    str = limpaTexto(str, "<br><br><br>")
    str = limpaTexto(str, "<br><br>")
    str = limpaTexto(str, "<br>")
     
    return str

def limpaTextoErrado (str):
    str =str.replace("</br>", "<br>")
    str =str.replace("<br/>", "<br>")
    str =str.replace("<br />", "<br>")
    str =str.replace("</ br>", "<br>")
    str =str.replace(" <br>", "<br>")
    str =str.replace(" <br>", "<br>")
    str =str.replace(" </div><br>", "</div>")
    str =str.replace(" <br><div", "<div")
    str =str.replace("&nbsp;", " ")
    str =str.replace('<font color="#ff0000"><b>Errado</b></font>',"Errado")
    str =str.replace('<font color="#ff0000">Errado</font>',"Errado")
    str =str.replace('<font color="#ff0000"><b>Errada</b></font>',"Errado")
    str =str.replace('<font color="#ff0000">Errada</font>',"Errado")
    str =str.replace("Gabarito: Errado.<br><br>","Gabarito: Errado.")
    str =str.replace("Gabarito: Errado.<br>","Gabarito: Errado.")
    str =str.replace("Gabarito: Errado<br><br>","Gabarito: Errado.")
    str =str.replace("Gabarito: Errado<br>","Gabarito: Errado.")
    
    str =str.replace("<br><br>Gabarito: Errado","Gabarito: Errado")
    str =str.replace("<br>Gabarito: Errado","Gabarito: Errado")
    
    str = limpaTextoInicio(str, "Gabarito: Errado.<br><br>")
    str = limpaTextoInicio(str, "Gabarito: Errado<br><br>")
    str = limpaTextoInicio(str, "Gabarito: Errado.<br>")
    str = limpaTextoInicio(str, "Gabarito: Errado<br>")
    str = limpaTextoInicio(str, "Gabarito: Errado.")
    str = limpaTextoInicio(str, "Gabarito: Errado")
    str = limpaTextoInicio(str, "Errado.<br><br>")
    str = limpaTextoInicio(str, "Errado.<br>")
    str = limpaTextoInicio(str, "Errado.")
    str = limpaTextoInicio(str, "Errado!<br><br>")
    str = limpaTextoInicio(str, "Errado!<br>")
    str = limpaTextoInicio(str, "Errado!")
    str = limpaTextoInicio(str, "Errado<br><br>")
    str = limpaTextoInicio(str, "Errado<br>")
    str = limpaTextoInicio(str, "Errado")
    
    str = limpaTextoFinal(str, "Gabarito: Errado.")
    str = limpaTextoFinal(str, "Gabarito: Errado")
    
    str = limpaTextoInicio(str, "Gabarito: Errada.")
    str = limpaTextoInicio(str, "Gabarito: Errada")
    str = limpaTextoInicio(str, "Errada.<br><br>")
    str = limpaTextoInicio(str, "Errada.<br>")
    str = limpaTextoInicio(str, "Errada!<br><br>")
    str = limpaTextoInicio(str, "Errada!<br>")
    str = limpaTextoInicio(str, "Errada<br><br>")
    str = limpaTextoInicio(str, "Errada<br>")
    str = limpaTextoFinal(str, "Gabarito: Errada.")
    str = limpaTextoFinal(str, "Gabarito: Errada")
    
    str = str.replace ("<div>Gabarito: Errado.</div>","")
    str = str.replace ("<div>Gabarito: Errado</div>","")
    str = str.replace ("<div>Gabarito: ERRADO.</div>","")
    str = str.replace ("<div>Gabarito: ERRADO</div>","")
    str = str.replace ("<div>Gabarito: Errada.</div>","")
    str = str.replace ("<div>Gabarito: Errada</div>","")
    str = str.replace ("<div>Gabarito: ERRADA.</div>","")
    str = str.replace ("<div>Gabarito: ERRADA</div>","")    
    return str

def adicionaTextoAntes(str, textoAdicional):

    return textoAdicional + str

def adicionaTextoDepois(str, textoAdicional):
    
    return  str + textoAdicional

def addGabaritoCerto(str):
    str = limpaTextoCerto(str)
    str = limpaTextoCerto(str)
    
    gab = """Gabarito:&nbsp;<font color="#0000ff"><b>Certo</b></font>.<br><br>"""

    str = adicionaTextoAntes(str, gab)

    gab = """<br><br>Gabarito:&nbsp;<font color="#0000ff"><b>Certo</b></font>."""

    str = adicionaTextoDepois(str, gab)

    return str

def addGabaritoErrado(str):
    str = limpaTextoErrado(str)
    str = limpaTextoErrado(str)

    gab = """Gabarito:&nbsp;<font color="#ff0000"><b>Errado</b></font>.<br><br>"""

    str = adicionaTextoAntes(str, gab)

    gab = """<br><br>Gabarito:&nbsp;<font color="#ff0000"><b>Errado</b></font>."""

    str = adicionaTextoDepois(str, gab)

    return str


def adicionaGabaritoCerto(self):
    """ Adiciona o gabarito ao campo que está sendo editado atualmente"""
    self.saveNow();
    self.mw.checkpoint(_("Adiciona Gabarito Certo"))
    text = self.note.fields[1]
    self.note.fields[1] = addGabaritoCerto(text)
    self.stealFocus = True;
    self.loadNote();

def adicionaGabaritoErrado(self):
    """ Adiciona o gabarito ao campo que está sendo editado atualmente"""
    self.saveNow();
    self.mw.checkpoint(_("Adiciona Gabarito Errado"))
    text = self.note.fields[1]
    self.note.fields[1] = addGabaritoErrado(text)
    self.stealFocus = True;
    self.loadNote();

def setupButtons(self):
    """ Adiciona os atalhos de teclado e os botões ao editor de notas"""
    
    icons_dir = os.path.join(mw.pm.addonFolder(), 'add_Gabarito', 'icons')
    b = self._addButton("addGabaritoErrado", lambda s=self: adicionaGabaritoErrado(self),
            text=" ", tip="Adiciona o Gabarito Errado(Ctrl+Shift+ae)", key="Ctrl+Shift+ae")
    b.setIcon(QIcon(os.path.join(icons_dir, 'errado.png')))
    
    c = self._addButton("addGabaritoCerto", lambda s=self: adicionaGabaritoCerto(self),
            text=" ", tip="Adiciona o Gabarito Certo (Ctrl+Shift+ac)", key="Ctrl+Shift+ac")
    c.setIcon(QIcon(os.path.join(icons_dir, 'certo.png')))

def adicionaGabaritoCertoEmLote(self):
    """ Performs search-and-replace on selected notes """
    nids = self.selectedNotes()
    if not nids:
        return
    # Allow undo
    self.mw.checkpoint(_("Adiciona Gabarito"))
    self.mw.progress.start()
    # Not sure if beginReset is required
    self.model.beginReset()
    for nid in nids:
        nota = mw.col.getNote(nid)
        text = nota.fields[1]
        nota.fields[1] = addGabaritoCerto(text)
        nota.stealFocus = True;
        nota.flush()


    self.model.endReset()
    self.mw.progress.finish()
    # Display a progress meter
    showInfo("Notas Atualizadas")

def adicionaGabaritoErradoEmLote(self):
    """ Performs search-and-replace on selected notes """
    nids = self.selectedNotes()
    if not nids:
        return
    # Allow undo
    self.mw.checkpoint(_("Adiciona Gabarito"))
    self.mw.progress.start()
    # Not sure if beginReset is required
    self.model.beginReset()
    for nid in nids:
        nota = mw.col.getNote(nid)
        text = nota.fields[1]
        nota.fields[1] = addGabaritoErrado(text)
        nota.stealFocus = True;
        nota.flush()


    self.model.endReset()
    self.mw.progress.finish()
    # Display a progress meter
    showInfo("Notas Atualizadas")

def addMenuItem(self):
    """ Adds hook to the Edit menu in the note browser """
    action = QAction("Adiciona Gabarito - Certo", self)
    self.adicionaGabaritoCertoEmLote = adicionaGabaritoCertoEmLote
    self.connect(action, SIGNAL("triggered()"), lambda s=self: adicionaGabaritoCertoEmLote(self))
    self.form.menuEdit.addAction(action)
    
    action = QAction("Adiciona Gabarito - Errado", self)
    self.adicionaGabaritoErradoEmLote = adicionaGabaritoErradoEmLote
    self.connect(action, SIGNAL("triggered()"), lambda s=self: adicionaGabaritoErradoEmLote(self))
    self.form.menuEdit.addAction(action)
    
# Add-in hook; called by the AQT Browser object when it is ready for the add-on to modify the menus
addHook('browser.setupMenus', addMenuItem)

Editor.adicionaGabaritoCerto = adicionaGabaritoCerto
Editor.adicionaGabaritoErrado = adicionaGabaritoErrado
Editor.setupButtons = wrap(Editor.setupButtons, setupButtons)

