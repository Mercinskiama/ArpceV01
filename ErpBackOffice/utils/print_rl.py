
from django.http import HttpResponse



from reportlab.lib import colors,utils
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter,A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm,mm
from reportlab.platypus import Paragraph, Table, TableStyle, Image, Spacer, SimpleDocTemplate,PageBreak
from reportlab.graphics import shapes
from reportlab.pdfgen import canvas
from reportlab.platypus.flowables import Flowable
import os
from django.conf import settings
from ErpBackOffice.utils.trad import trad
from ErpBackOffice.utils.separateur import get_monetary, get_monetary_rounded

from io import BytesIO

#---------------enregistre font
from reportlab.pdfbase.pdfmetrics import registerFont,registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
#registerFont(TTFont('MonotypeCorsiva','media/regideso/Monotype_Corsiva.ttf'))
#registerFontFamily('MonotypeCorsiva',normal='MonotypeCorsiva',bold='MonotypeCorsiva-Bold',italic='MonotypeCorsiva-Italic',boldItalic='MonotypeCorsiva-BoldItalic')

registerFont(TTFont('Carlito', os.path.join(settings.CSS_DIR,'media/regideso/google-crosextrafonts-carlito-20130920/Carlito-Regular.ttf').replace("\\", "/")))
registerFont(TTFont('Carlito-Bold', os.path.join(settings.CSS_DIR,'media/regideso/google-crosextrafonts-carlito-20130920/Carlito-Bold.ttf').replace("\\", "/")))


from functools import partial
from reportlab.platypus.doctemplate import Indenter

import pyqrcodeng
import base64

from PIL import Image as pil_img
def img_opacity(val,tval):
    
	img = pil_img.open(val)
	img.putalpha(tval)  # Half alpha; alpha argument must be an int
	buffered = BytesIO()
	img.save(buffered, format="PNG")
	img_str = base64.b64encode(buffered.getvalue())
	img_str=img_str.decode('utf-8')
	img_str='data:image/png;base64,'+img_str
	buffered.close()
	
	return img_str

def make_base64_qr_code(val,mat):
	
	big_code = pyqrcodeng.create(val)
	
	#img_str = 'data:image/png;base64,{}'.format(big_code.png_as_base64_str(scale=6))
	chmt=settings.MEDIA_ROOT+'/'+f'{mat}.png'
	imgqr=big_code.png(chmt, scale=6)
	
	return chmt

def dgtcp_fiche_agent(employee, request=None):
	elements=[]
	media_dir = os.path.join(settings.CSS_DIR, "/static/media/dgtcp")
	#print(f"media_dir: {media_dir}")

	
	text_s_entete = ParagraphStyle(
			name='text_s_entete',
			fontName='Carlito-Bold',
			fontSize=13,
			leading=10,
			alignment=TA_LEFT,
			backColor='#cccccc',
			textColor= '#000000',
			)
	text_s_no_bck = ParagraphStyle(
			name='text_s_no_bck',
			fontName='Carlito-Bold',
			fontSize=13,
			leading=10,
			alignment=TA_LEFT,
			
			textColor= '#000000',
			)
	
	text_s = ParagraphStyle(
			name='text_s',
			fontName='Carlito',
			fontSize=12,
			leading=18,
			alignment=TA_LEFT,
			textColor= '#000000',
			)
	text_titre = ParagraphStyle(
			name='text_titre',
			fontName='Carlito-Bold',
			fontSize=20,
			leading=18,
			alignment=TA_CENTER,
			textColor= '#000000',
			)
	
	logo = os.path.join(settings.CSS_DIR,'media/regideso/entete2.png').replace("\\", "/")
	
	#im2 = Image(logo, width=12.5*cm, height=6.3*cm, mask='auto')
	cadre=shapes.Drawing(21*cm,4.3*cm)


	logo=shapes.Image(3*cm,0*cm, 12.5*cm,4.3*cm,logo)
	cadre.add(logo)
	
	matricule = f'{employee.matricule}'
	
	acte_sous_statut=f'{employee.acte_sous_statut}'
	date_naissance = ""
	if employee.date_naissance : date_naissance = employee.date_naissance.strftime("%d/%m/%Y")
	
	contents=matricule.strip().lower()+', '+date_naissance.strip().lower()+', '+acte_sous_statut.strip()
	qrel=make_base64_qr_code(contents,matricule)
	qr_lib=shapes.Image(0*cm,1.2*cm, 4*cm,3.5*cm,qrel)
	
	cadre.add(qr_lib)
	#im2.hAlign = 'CENTER'
	#elements.append(im2)
	elements.append(cadre)
	elements.append(Spacer(1, 20))
	elements.append(Paragraph("<u>FICHE DE COLLECTE D'INFORMATION PERSONNELLE</u>", style=text_titre))
	elements.append(Spacer(1, 20))
	
	elements.append(Paragraph('&nbsp;1 . IDENTITE DE L’AGENT<br /><br />', style=text_s_entete))
	elements.append(Spacer(1, 7))
	nom_complet = f'{employee.nom} {employee.postnom}'
	if len(nom_complet) <= 40: 
		n = 40 - len(nom_complet)
		for i in range(0,n): nom_complet = nom_complet + "&nbsp;"
  
	matricule = f'{employee.matricule}'
	if len(matricule) <= 20: 
		n = 20 - len(matricule)
		for i in range(0,n): matricule = matricule + "&nbsp;"
  
	genre = f'{employee.value_genre}'
	for i in range(0,30): genre = genre + "&nbsp;"
  
  
	lieu_naissance = f'{employee.lieu_naissance}'
	if len(lieu_naissance) <= 40: 
		n = 40 - len(lieu_naissance)
		for i in range(0,n): lieu_naissance = lieu_naissance + "&nbsp;"
  
	nom_pere = f'{employee.nom_pere}'
	if len(nom_pere) <= 40: 
		n = 40 - len(nom_pere)
		for i in range(0,n): nom_pere = nom_pere + "&nbsp;"
  
	province_origine = f'{employee.province_origine}'
	if len(province_origine) <= 40: 
		n = 40 - len(province_origine)
		for i in range(0,n): province_origine = province_origine + "&nbsp;"
  
	territoire_origine = f'{employee.territoire_origine}'
	if len(territoire_origine) <= 40: 
		n = 40 - len(territoire_origine)
		for i in range(0,n): territoire_origine = territoire_origine + "&nbsp;"

	date_naissance = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"  
	if employee.date_naissance : date_naissance = employee.date_naissance.strftime("%d/%m/%Y")

	date_mariage = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"  
	if employee.date_mariage : date_mariage = employee.date_mariage.strftime("%d/%m/%Y")
	
	date_divorse = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"  
	if employee.date_divorse : date_divorse = employee.date_divorse.strftime("%d/%m/%Y")

	date_deces_conjoint = ""  
	if employee.date_deces_conjoint : date_deces_conjoint = employee.date_deces_conjoint.strftime("%d/%m/%Y")
	
	conjoint_date_naissance = ""  
	if employee.conjoint and employee.conjoint.date_naissance  : conjoint_date_naissance = employee.conjoint.date_naissance.strftime("%d/%m/%Y")
	
	conjoint_lieu_naissance = ""  
	if employee.conjoint and employee.conjoint.lieu_naissance  : conjoint_lieu_naissance = str(employee.conjoint.lieu_naissance)+','
	
	conjoint_nom_complet = ""  
	if employee.conjoint and employee.conjoint.nom_complet  : conjoint_nom_complet = employee.conjoint.nom_complet
	
	date_mecanisation = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"  
	if employee.date_mecanisation : date_mecanisation = employee.date_mecanisation.strftime("%d/%m/%Y")

	date_acte_sous_statut = ""  
	if employee.date_acte_sous_statut : date_acte_sous_statut = employee.date_acte_sous_statut.strftime("%d/%m/%Y")
 
	date_titularisation = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"  
	if employee.date_titularisation : date_titularisation = employee.date_titularisation.strftime("%d/%m/%Y")
 
	est_mecanise = 'Non'
	if employee.est_mecanise: est_mecanise = 'Oui'
 
	concours = 'Non'
	if employee.passe_concours: concours = 'Oui'
 
	adresse = ''
	if employee.adresse: adresse = f'{employee.adresse}, '

	ville = ''
	if employee.ville: ville = f'Ville de {employee.ville}, '
 
	province = ''
	if employee.province: province = f'{employee.province}, '
 
	pays = ''
	if employee.pays: pays = f'{employee.pays}'
 
	adresse = f'{adresse}{ville}{province}{pays}'
 
	grade = ''
	if employee.grade: grade = f'{employee.grade}'
 
	fonction = ''
	if employee.fonction: fonction = f'{employee.fonction}'
 
	elements.append(Paragraph(f'''
							Nom et Post-nom : <span name="Carlito-Bold">{nom_complet}</span> Prénom : <span name="Carlito-Bold">{employee.prenom}</span>''', style=text_s))
	elements.append(Paragraph(f'''Matricule : <span name="Carlito-Bold">{matricule}</span>  Grade : <span name="Carlito-Bold">{grade}</span> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Fonction : <span name="Carlito-Bold">{fonction}</span>''', style=text_s))
	elements.append(Paragraph(f'''Sexe : <span name="Carlito-Bold">{genre}</span> Aptitude physique: <span name="Carlito-Bold">{employee.aptitude}</span>''', style=text_s))
	elements.append(Paragraph(f'''
							Adresse : <span name="Carlito-Bold">{adresse}</span>''', style=text_s))
	elements.append(Paragraph(f'''Lieu de Naissance : <span name="Carlito-Bold">{lieu_naissance}</span> Date de Naissance : <span name="Carlito-Bold">{date_naissance}</span> ''', style=text_s))
	elements.append(Paragraph(f'''Téléphone : <span name="Carlito-Bold">{employee.telephone}</span>''', style=text_s))
	elements.append(Paragraph(f'''Nom du Père : <span name="Carlito-Bold">{nom_pere}</span>   De la Mère : <span name="Carlito-Bold">{employee.nom_mere}</span>''', style=text_s))
	elements.append(Paragraph(f'''Province : <span name="Carlito-Bold">{province_origine}</span> Secteur : <span name="Carlito-Bold">{employee.secteur_origine}</span>''', style=text_s))
	elements.append(Paragraph(f'''Territoire : <span name="Carlito-Bold">{territoire_origine}</span>

							
							''', style=text_s))
	
	elements.append(Spacer(1, 9))
	
	elements.append(Paragraph('&nbsp;2. SITUATION FAMILLIALE ET MECANISATION<br /><br />', style=text_s_entete))
	elements.append(Spacer(1, 7))
	elements.append(Paragraph(f'''
							Etat civil : <span name="Carlito-Bold">{employee.value_etat_civil}</span> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Nom conjoint(e) :<span name="Carlito-Bold">{conjoint_nom_complet}</span><br /> 
    						Lieu et date de Naiss :<span name="Carlito-Bold">{conjoint_lieu_naissance}&nbsp;&nbsp;{conjoint_date_naissance}</span>&nbsp;&nbsp;&nbsp;&nbsp;
          					Date de mariage : <span name="Carlito-Bold">{date_mariage}</span><br />
               				Date divorce : <span name="Carlito-Bold">{date_divorse}</span> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Date décès conjoint(e) : <span name="Carlito-Bold">{date_deces_conjoint}</span> <br />
							Mécanisé : <span name="Carlito-Bold">{est_mecanise}</span> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Date de Mécanisation : <span name="Carlito-Bold">{date_mecanisation}</span> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Acte Mécanisation : <span name="Carlito-Bold">{employee.mecanisation}</span>''', style=text_s))       
							
	
	elements.append(Spacer(1, 9))
	elements.append(Paragraph('''Enfants
							&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
							Enfants S/T''', style=text_s_no_bck))
	
	elements.append(Spacer(1, 9))
	Dinsert=[]
	enf=''
	el=employee.enfant
	#print(el)
	last_item = len(el)-1
	for index,item in enumerate(el):
		enf=str(enf)+str(item)+'<br />'
		if index != last_item:
			enf=str(enf)+'<br />'
	if len(el) < 3: 
		n = 3 - len(el)
		for i in range(0,n): enf=str(enf)+'<br />'
	col1=Paragraph(f'''{enf}''', style=text_s)
	
	enf=''
	el=employee.enfant_st
	#print(el)
	last_item = len(el)-1
	for index,item in enumerate(el):
		enf=str(enf)+str(item)+'<br />'
		if index != last_item:
			enf=str(enf)+'<br />'
	if len(el) < 3: 
		n = 3 - len(el)
		for i in range(0,n): enf=str(enf)+'<br />'
	col2=Paragraph(f'''{enf}''', style=text_s)

	lin1=[col1,'',col2]
	Dinsert.append(lin1)

	

	table=Table(Dinsert, hAlign='LEFT',vAlign='TOP',colWidths=[9*cm,1*cm,9*cm])
	table.setStyle(TableStyle([
			('LEFTPADDING', (0, 0), (-1, -1), 2*mm),
			('RIGHTPADDING', (0, 0), (-1, -1), 2*mm),
			('TOPPADDING', (0, 0), (-1, -1), 2*mm),
			('BOTTOMPADDING', (0, 0), (-1, -1), 2*mm),
			('VALIGN', (0, 0), (-1, -1), 'TOP'),
			('ALIGN', (0, 0), (-1, -1), 'LEFT'),
			
			('BOX', (0, 0), (0, 0),0.5,'#000000'),
			('BOX', (2, 0), (2, 0),0.5,'#000000'),
			]))
	elements.append(table)
	
	
	elements.append(Spacer(1, 6))
	
	elements.append(Paragraph('''
					3. STRUCTURE

					''', style=text_s))
	
	elements.append(Spacer(1, 6))
	
	direction = ""
	if employee.direction : direction = employee.direction.name
	division = ""
	if employee.division : division = employee.division.name
	bureau = ""
	if employee.bureau : bureau = employee.bureau.name
	elements.append(Paragraph(f'''
					Ministère : <span name="Carlito-Bold">{employee.ministere}</span><br />
					Direction : <span name="Carlito-Bold">{direction}</span><br /> 
					Division : <span name="Carlito-Bold">{division}</span><br />
					Bureau : <span name="Carlito-Bold">{bureau}</span><br />
					Poste organique : <span name="Carlito-Bold">{employee.poste_organique}</span>

					''', style=text_s))
	
	#elements.append(Spacer(1, 9))
	elements.append(PageBreak())
	elements.append(Paragraph('&nbsp;4. SITUATION ADMINISTRATIVE<br /><br />', style=text_s_entete))
	elements.append(Spacer(1, 6))
	grade = ""
	if employee.grade : grade = employee.grade
	elements.append(Paragraph(f'''
							Acte sous statut : <span name="Carlito-Bold">{employee.acte_sous_statut}</span> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Date : <span name="Carlito-Bold">{date_acte_sous_statut}</span> &nbsp;&nbsp;&nbsp; Concours : <span name="Carlito-Bold">{concours}</span><br />
							Grade : <span name="Carlito-Bold">{grade}</span>  Période Probation : <span name="Carlito-Bold">{employee.periode_probation}</span> <br />
							Durée :<span name="Carlito-Bold">{employee.duree_periode_probation}</span> / Date titularisation : <span name="Carlito-Bold">{date_titularisation}</span><br /><br />

							''', style=text_s))

	#elements.append(PageBreak())
	text_dependance = ParagraphStyle(
			name='text_dependance',
			fontName='Carlito-Bold',
			fontSize=9,
			leading=9,
			alignment=TA_LEFT,
			textColor= '#000000',
			)
	elements.append(Paragraph('&nbsp;5. FORMATION<br /><br />', style=text_s_entete))
	Dinsert=[]
	lin1=['Formations','Filière','Niveau Et.','Titre','Institution','Pays','Année']
	Dinsert.append(lin1)

	el=employee.formation
	for item in el:
		lin1=[Paragraph(f'{item.name}', style=text_dependance),Paragraph(f'{item.filiere}', style=text_dependance),Paragraph(f'{item.niveau}', style=text_dependance),Paragraph(f'{item.titre}', style=text_dependance),Paragraph(f'{item.institution}', style=text_dependance),Paragraph(f'{item.pays_naissance}', style=text_dependance),Paragraph(f'{item.annee}', style=text_dependance)]
		Dinsert.append(lin1)
	if len(el) < 3: 
		n = 3 - len(el)
		for i in range(0,n):
			lin1=['','','','','','','']
			Dinsert.append(lin1)
	
			
	

	table=Table(Dinsert, hAlign='LEFT',vAlign='TOP',colWidths=[3.3*cm,4*cm,2*cm,2*cm,4*cm,3.1*cm,1.2*cm])
	table.setStyle(TableStyle([
			('LEFTPADDING', (0, 0), (-1, -1), 2*mm),
			('RIGHTPADDING', (0, 0), (-1, -1), 2*mm),
			('TOPPADDING', (0, 0), (-1, -1), 1*mm),
			('BOTTOMPADDING', (0, 0), (-1, -1), 1*mm),
			('TOPPADDING', (0, 0), (-1, 0), 0.5*mm),
			('BOTTOMPADDING', (0, 0), (-1, 0), 0.5*mm),
			('VALIGN', (0, 0), (-1, -1), 'TOP'),
			('ALIGN', (0, 0), (-1, -1), 'LEFT'),
			('ALIGN', (0, 0), (-1, 0), 'CENTER'),
			
			('TEXTCOLOR', (0, 0), (-1, -1), '#000000'),
			('FONTNAME', (0, 0), (-1, -1), 'Carlito-Bold'),
			('FONTSIZE', (0, 0), (-1, -1), 9),
			
			('GRID', (0, 0), (-1, 0),0.3,'#000000'),
			('BOX', (0, 1), (0, -1),0.3,'#000000'),
			('BOX', (1, 1), (1, -1),0.3,'#000000'),
			('BOX', (2, 1), (2, -1),0.3,'#000000'),
			('BOX', (3, 1), (3, -1),0.3,'#000000'),
			('BOX', (4, 1), (4, -1),0.3,'#000000'),
			('BOX', (5, 1), (5, -1),0.3,'#000000'),
			('BOX', (6, 1), (6, -1),0.3,'#000000'),
			]))
	elements.append(table)
	
	elements.append(Spacer(1, 10))
	
	elements.append(Paragraph('&nbsp;6. NOMINATIONS <br /><br />', style=text_s_entete))
	Dinsert=[]
	lin1=['Acte Nomination','Date','Fonction','Type Nom','Commission Affectation','Date Com']
	Dinsert.append(lin1)
	
	el=employee.nomination
	for item in el:
		date_nomination = item.date_nomination.strftime("%d/%m/%Y")
		date_commission = item.date_commission.strftime("%d/%m/%Y")
		lin1=[Paragraph(f'{item.name}', style=text_dependance),Paragraph(f'{date_nomination}', style=text_dependance),Paragraph(f'{item.fonction}', style=text_dependance),Paragraph(f'{item.type}', style=text_dependance),Paragraph(f'{item.commission}', style=text_dependance),Paragraph(f'{date_commission}', style=text_dependance)]
		Dinsert.append(lin1)
	if len(el) < 3: 
		n = 3 - len(el)
		for i in range(0,n):
			lin1=['','','','','','']
			Dinsert.append(lin1)
	

	table=Table(Dinsert, hAlign='LEFT',vAlign='TOP',colWidths=[4.5*cm,2*cm,2.1*cm,4.5*cm,4.5*cm,2*cm])
	table.setStyle(TableStyle([
			('LEFTPADDING', (0, 0), (-1, -1), 2*mm),
			('RIGHTPADDING', (0, 0), (-1, -1), 2*mm),
			('TOPPADDING', (0, 0), (-1, -1), 1*mm),
			('BOTTOMPADDING', (0, 0), (-1, -1), 1*mm),
			('TOPPADDING', (0, 0), (-1, 0), 0.5*mm),
			('BOTTOMPADDING', (0, 0), (-1, 0), 0.5*mm),
			('VALIGN', (0, 0), (-1, -1), 'TOP'),
			('ALIGN', (0, 0), (-1, -1), 'LEFT'),
			('ALIGN', (0, 0), (-1, 0), 'CENTER'),
			
			('TEXTCOLOR', (0, 0), (-1, -1), '#000000'),
			('FONTNAME', (0, 0), (-1, -1), 'Carlito-Bold'),
			('FONTSIZE', (0, 0), (-1, -1), 9),
			
			('GRID', (0, 0), (-1, 0),0.3,'#000000'),
			('BOX', (0, 1), (0, -1),0.3,'#000000'),
			('BOX', (1, 1), (1, -1),0.3,'#000000'),
			('BOX', (2, 1), (2, -1),0.3,'#000000'),
			('BOX', (3, 1), (3, -1),0.3,'#000000'),
			('BOX', (4, 1), (4, -1),0.3,'#000000'),
			('BOX', (5, 1), (5, -1),0.3,'#000000'),
			
			]))
	elements.append(table)
	
	
	elements.append(Spacer(1, 10))
	
	elements.append(Paragraph('&nbsp;7. POSITIONS<br /><br />', style=text_s_entete))
	Dinsert=[]
	lin1=['Position','Référence Acte','Organisation','Date Détachement','Durée']
	Dinsert.append(lin1)
	
	el=employee.position
	for item in el:
		date_detachement = item.date_detachement.strftime("%d/%m/%Y")
		
		lin1=[Paragraph(f'{item.name}', style=text_dependance),Paragraph(f'{item.reference}', style=text_dependance),Paragraph(f'{item.organisation}', style=text_dependance),Paragraph(f'{date_detachement}', style=text_dependance),Paragraph(f'{item.duree}', style=text_dependance)]
		Dinsert.append(lin1)
	if len(el) < 3: 
		n = 3 - len(el)
		for i in range(0,n):
			lin1=['','','','','']
			Dinsert.append(lin1)
	

	table=Table(Dinsert, hAlign='LEFT',vAlign='TOP',colWidths=[4.5*cm,5*cm,5.5*cm,2.6*cm,2*cm])
	table.setStyle(TableStyle([
			('LEFTPADDING', (0, 0), (-1, -1), 2*mm),
			('RIGHTPADDING', (0, 0), (-1, -1), 2*mm),
			('TOPPADDING', (0, 0), (-1, -1), 1*mm),
			('BOTTOMPADDING', (0, 0), (-1, -1), 1*mm),
			('TOPPADDING', (0, 0), (-1, 0), 0.5*mm),
			('BOTTOMPADDING', (0, 0), (-1, 0), 0.5*mm),
			('VALIGN', (0, 0), (-1, -1), 'TOP'),
			('ALIGN', (0, 0), (-1, -1), 'LEFT'),
			('ALIGN', (0, 0), (-1, 0), 'CENTER'),
			
			('TEXTCOLOR', (0, 0), (-1, -1), '#000000'),
			('FONTNAME', (0, 0), (-1, -1), 'Carlito-Bold'),
			('FONTSIZE', (0, 0), (-1, -1), 9),
			
			('GRID', (0, 0), (-1, 0),0.3,'#000000'),
			('BOX', (0, 1), (0, -1),0.3,'#000000'),
			('BOX', (1, 1), (1, -1),0.3,'#000000'),
			('BOX', (2, 1), (2, -1),0.3,'#000000'),
			('BOX', (3, 1), (3, -1),0.3,'#000000'),
			('BOX', (4, 1), (4, -1),0.3,'#000000'),
			
			
			]))
	elements.append(table)
	
	
	
	elements.append(Spacer(1, 10))
	
	elements.append(Paragraph('&nbsp;8. REMUNERATIONS & PRIMES RECUES<br /><br />', style=text_s_entete))
	Dinsert=[]
	lin1=['Rém. & primés reçues','Motif Blocage','Date blocage','Acte blocage','Date déblocage','Acte déblocage']
	Dinsert.append(lin1)
	
	el=employee.prime
	for item in el:
		date_blocage = item.date_blocage.strftime("%d/%m/%Y")
		date_deblocage = item.date_deblocage.strftime("%d/%m/%Y")
		lin1=[Paragraph(f'{item.name}', style=text_dependance),Paragraph(f'{item.motif_blocage}', style=text_dependance),Paragraph(f'{date_blocage}', style=text_dependance),Paragraph(f'{item.acte_blocage}', style=text_dependance),Paragraph(f'{date_deblocage}', style=text_dependance),Paragraph(f'{item.acte_deblocage}', style=text_dependance)]
		Dinsert.append(lin1)
	if len(el) < 3: 
		n = 3 - len(el)
		for i in range(0,n):
			lin1=['','','','','','']
			Dinsert.append(lin1)
	

	table=Table(Dinsert, hAlign='LEFT',vAlign='TOP',colWidths=[4*cm,5*cm,2*cm,3.3*cm,2*cm,3.3*cm])
	table.setStyle(TableStyle([
			('LEFTPADDING', (0, 0), (-1, -1), 2*mm),
			('RIGHTPADDING', (0, 0), (-1, -1), 2*mm),
			('TOPPADDING', (0, 0), (-1, -1), 1*mm),
			('BOTTOMPADDING', (0, 0), (-1, -1), 1*mm),
			('TOPPADDING', (0, 0), (-1, 0), 0.5*mm),
			('BOTTOMPADDING', (0, 0), (-1, 0), 0.5*mm),
			('VALIGN', (0, 0), (-1, -1), 'TOP'),
			('ALIGN', (0, 0), (-1, -1), 'LEFT'),
			('ALIGN', (0, 0), (-1, 0), 'CENTER'),
			
			('TEXTCOLOR', (0, 0), (-1, -1), '#000000'),
			('FONTNAME', (0, 0), (-1, -1), 'Carlito-Bold'),
			('FONTSIZE', (0, 0), (-1, -1), 9),
			
			('GRID', (0, 0), (-1, 0),0.3,'#000000'),
			('BOX', (0, 1), (0, -1),0.3,'#000000'),
			('BOX', (1, 1), (1, -1),0.3,'#000000'),
			('BOX', (2, 1), (2, -1),0.3,'#000000'),
			('BOX', (3, 1), (3, -1),0.3,'#000000'),
			('BOX', (4, 1), (4, -1),0.3,'#000000'),
			('BOX', (5, 1), (5, -1),0.3,'#000000'),
			
			]))
	elements.append(table)
	
	
	elements.append(Spacer(1, 10))
	
	elements.append(Paragraph('&nbsp;9. COTATION<br /><br />', style=text_s_entete))
	Dinsert=[]
	lin1=['Date de cotation','Mention','Nom Autorité']
	Dinsert.append(lin1)
	
	el=employee.evaluation
	for item in el:
		date_deblocage = item.date_deblocage.strftime("%d/%m/%Y")
		
		lin1=[Paragraph(f'{date_deblocage}', style=text_dependance),Paragraph(f'{item.mention}', style=text_dependance),Paragraph(f'{item.autorite}', style=text_dependance)]
		Dinsert.append(lin1)
	if len(el) < 3: 
		n = 3 - len(el)
		for i in range(0,n):
			lin1=['','','']
			Dinsert.append(lin1)
	

	table=Table(Dinsert, hAlign='LEFT',vAlign='TOP',colWidths=[3*cm,4.6*cm,12*cm])
	table.setStyle(TableStyle([
			('LEFTPADDING', (0, 0), (-1, -1), 2*mm),
			('RIGHTPADDING', (0, 0), (-1, -1), 2*mm),
			('TOPPADDING', (0, 0), (-1, -1), 1*mm),
			('BOTTOMPADDING', (0, 0), (-1, -1), 1*mm),
			('TOPPADDING', (0, 0), (-1, 0), 0.5*mm),
			('BOTTOMPADDING', (0, 0), (-1, 0), 0.5*mm),
			('VALIGN', (0, 0), (-1, -1), 'TOP'),
			('ALIGN', (0, 0), (-1, -1), 'LEFT'),
			('ALIGN', (0, 0), (-1, 0), 'CENTER'),
			
			('TEXTCOLOR', (0, 0), (-1, -1), '#000000'),
			('FONTNAME', (0, 0), (-1, -1), 'Carlito-Bold'),
			('FONTSIZE', (0, 0), (-1, -1), 9),
			
			('GRID', (0, 0), (-1, 0),0.3,'#000000'),
			('BOX', (0, 1), (0, -1),0.3,'#000000'),
			('BOX', (1, 1), (1, -1),0.3,'#000000'),
			('BOX', (2, 1), (2, -1),0.3,'#000000'),
			
			]))
	elements.append(table)
	
	elements.append(Spacer(1, 5))
	
	if employee.fichier_piece_identite:
		try:
			im_fichier_piece_identite = Image(img_opacity(employee.fichier_piece_identite.path,60), width=8.5*cm, height=4*cm, mask= 'auto')
			im_fichier_piece_identite.hAlign = 'CENTER'
			elements.append(im_fichier_piece_identite)
			elements.append(Spacer(1, 5))
		except Exception as e:
			print(e)
			pass
	date_cr = ""  
	if employee.update_date : date_cr = employee.update_date.strftime("%d/%m/%Y")
	elements.append(Paragraph(f'''
					&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
					&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
					&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
					&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
					&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
					&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
					Fait à Kinshasa, le&nbsp;{date_cr}
					''', style=text_s))
	
	
	elements.append(Spacer(1, 1))
	elements.append(Paragraph('''
					Signature de l’Agent
					&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
					&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
					&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
					&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
					Signature de l’Autorité
					''', style=text_s_no_bck))

	buffer = BytesIO()
	doc = SimpleDocTemplate(buffer, pagesize=letter,leftMargin=1*cm,rightMargin=0.5*cm,topMargin=0.5*cm,bottomMargin=0.3*cm )
	doc.build(elements)
	pdf = buffer.getvalue()
	buffer.close()
	os.remove(qrel)
	response = HttpResponse(pdf, content_type='application/pdf')
	response['Content-Disposition'] = 'inline;filename=dgtcp_fiche_agent.pdf'
	return response

def draw_paragraphcontent( can, msg, x, y, max_width, max_height, color, fontsize, text_align=TA_CENTER,fontname='openbd',leadingset=10,):
	message_style = ParagraphStyle('Normal', fontName=fontname, textColor=color, fontSize=fontsize,alignment=text_align,leading=leadingset)
	#message = msg.replace('\n', '<br />')
	message = msg
	message = Paragraph(message, style=message_style)
	w, h = message.wrap(max_width, max_height)
	message.drawOn(can, x, y - h)
	pass

def recu_caisse(operation_caisse, request=None):
	buffer = BytesIO()
	doc = canvas.Canvas(buffer, pagesize=letter)
	doc.rect(1*cm,14*cm,20*cm,13*cm)
	doc.setStrokeColorRGB(0,0,0)
	doc.line(5*cm,23.8*cm,5*cm,26.8*cm)
	doc.line(1.1*cm,23.7*cm,20.8*cm,23.7*cm)
	logo = os.path.join(settings.CSS_DIR,'media/regideso/logo.png').replace("\\", "/")
	doc.drawImage(logo,1.2*cm,24*cm, width=3*cm,height=2.5*cm,mask='auto')
	msg='''REGIE DE DISTRIBUTION D'EAU DE LA REPUBLIQUE DEMOCRATIQUE DU CONGO<br/>DIRECTION GENERALE'''
	draw_paragraphcontent(doc, msg,5.2*cm, 26.2*cm, 8*cm, 4*cm, "#000000", 11, TA_CENTER,'Helvetica-Bold',15)
	
	doc.setFont("Helvetica-Bold", 13)
	devise = operation_caisse.devise.code_iso
	doc.drawString(14.9*cm,26*cm,devise.upper())
	doc.setFillColor("#f2f2f2")
	doc.rect(16*cm,25.65*cm,4.5*cm,1*cm,fill=1)
	doc.setFillColor("#000000")
	montant = get_monetary_rounded(operation_caisse.montant)
	doc.drawString(16.5*cm,26*cm,montant)
	
	doc.drawString(14.9*cm,24*cm,"N° ")
	numero_operation = operation_caisse.code
	doc.drawString(15.8*cm,24*cm,numero_operation)
	
	nom_caisse = f"{operation_caisse.caisse.name}".upper()
	msg=f'''<u>RECU {nom_caisse}</u>'''
	draw_paragraphcontent(doc, msg,0*cm, 23.3*cm, 23*cm, 1*cm, "#000000", 14, TA_CENTER,'Helvetica-Bold')
	
	nom_complet = operation_caisse.partenaire.nom_complet.upper() if operation_caisse.partenaire else 'ANONYME'
	msg=f'''<span name="Helvetica-Bold" color="#000000" size="13">RECU de Mr/Cit. : </span> {nom_complet}'''
	draw_paragraphcontent(doc, msg,1.2*cm, 22.3*cm, 20*cm, 1*cm, "#000000", 12, TA_LEFT,'Helvetica-Bold',20)
	
	doc.setFont("Helvetica", 13)
	doc.drawString(17.3*cm,21*cm,'la somme de:')
	doc.drawString(17.6*cm,20.4*cm,'(en lettres)')
	
	
	doc.setFillColor("#f2f2f2")
	doc.rect(1.2*cm,18.6*cm,19*cm,1.3*cm,fill=1)
	doc.setFillColor("#000000")
	montant_lettre = trad.trad(operation_caisse.montant)
	draw_paragraphcontent(doc, montant_lettre,1.2*cm, 19.55*cm, 19*cm, 1*cm, "#000000", 12, TA_CENTER,'Helvetica',15)
	
	
	pour = operation_caisse.name
	msg=f'''<span name="Helvetica-Bold" color="#000000" size="13">Pour: </span> {pour}'''
	draw_paragraphcontent(doc, msg,1.2*cm, 18*cm, 20*cm, 1*cm, "#000000", 12, TA_LEFT,'Helvetica',15)
	
	
	msg=f'''Kinshasa, le 14/05/2022 
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
	Noms et Signature du Caissier'''
	draw_paragraphcontent(doc, msg,1.2*cm, 16.5*cm, 20*cm, 1*cm, "#000000", 12, TA_LEFT,'Helvetica-Bold',15)


	doc.showPage()
	doc.save()
	pdf = buffer.getvalue()
	buffer.close()
	#response.write(pdf)

	response = HttpResponse(pdf, content_type='application/pdf')
	response['Content-Disposition'] = 'inline;filename=recu_caisse.pdf'
	return response

def bordereau_des_encaissement(session_caisse, request=None):  
    buffer = BytesIO()
    elements=[]

    cadre=shapes.Drawing(19*cm,5*cm)

    text_regideso=shapes.String(0*mm,4.3*cm,'REGIDESO',fontName="Helvetica-Bold",fontSize=19,fillColor="#000000")
    cadre.add(text_regideso)
    text_s=shapes.String(0*mm,3.3*cm,'D.U KINSHASA NORD',fontName="Helvetica-Bold",fontSize=13,fillColor="#000000")
    cadre.add(text_s)
    text_s=shapes.String(0*mm,2.6*cm,'Secteur: ',fontName="Helvetica-Bold",fontSize=13,fillColor="#000000")
    cadre.add(text_s)
    text_s=shapes.String(0*mm,1.9*cm,'Code: ',fontName="Helvetica-Bold",fontSize=13,fillColor="#000000")
    cadre.add(text_s)

    text_s=shapes.String(4.5*cm,0.8*cm,'BORDEREAUX DES ENCAISSEMENTS',fontName="Helvetica-Bold",fontSize=17,fillColor="#000000")
    cadre.add(text_s)
    
    text_s=shapes.String(7.5*cm,0*cm,'Journée de ............',fontName="Helvetica-Bold",fontSize=13,fillColor="#000000")
    cadre.add(text_s)
    '''ligne=shapes.Line(0*cm,0*cm, 15*cm,0.7*cm,strokeColor="#000000", strokeWidth=0*mm)
    cadre.add(ligne)'''

    elements.append(cadre)

    styleDetail = ParagraphStyle(
                name='xxxstyle',
                fontName='Helvetica',
                fontSize=14,
                leading=21,
                alignment=TA_LEFT
                )

    elements.append(Spacer(1, 10))


    Dinsert=[]
    entete1=['CODE','N° ACQUIT','N° ABONNE','PERIODE','N° FACTURE','MONTANT','ESCOMPTE']
    Dinsert.append(entete1)
    
    for x in range(1,17):
        ligne=['','','','','','','']
        Dinsert.append(ligne)

    lignetot=['','','','','','58000','']
    Dinsert.append(lignetot)
    
    
    table=Table(Dinsert, hAlign='LEFT',vAlign='TOP',colWidths=[1.8*cm,3.3*cm,3.3*cm,2*cm,3.3*cm,3.3*cm,3.3*cm])
    table.setStyle(TableStyle([
            ('LEFTPADDING', (0, 0), (-1, -1), 2*mm),
            ('RIGHTPADDING', (0, 0), (-1, -1), 2*mm),
            ('TOPPADDING', (0, 0), (-1, -1), 2*mm),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2*mm),
            ('TOPPADDING', (0, 0), (-1, 0), 4*mm),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 4*mm),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('TEXTCOLOR', (0, 0), (-1, -1), '#000000'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('GRID', (0, 0), (-1, -2), 0.5, '#000000'),
            ('GRID', (5, -1), (5, -1), 0.5, '#000000'),
            ('FONTNAME', (5, -1), (5, -1), 'Helvetica-Bold'),
            ('ALIGN', (5, 1), (5, -1), 'RIGHT'),
            
            
            ]))
    elements.append(table)



    elements.append(Spacer(1, 10))

    foot=Paragraph('''
                   NOM DU CASSIER .................................   <br />
                   SIGNATURE ............................   <br />
                   NOM DU RESPONSABLE COMMERCIAL ...............................<br />
                   SIGNATURE
                   ''', style=styleDetail)
    elements.append(foot)

    doc = SimpleDocTemplate(buffer, pagesize=letter,leftMargin=0.5*cm,topMargin=0.5*cm,bottomMargin=0.5*cm )
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline;filename=bordereau_encaissement.pdf'
    return response

def bordereau_des_decaissement(session_caisse, request=None):  
    buffer = BytesIO()
    elements=[]

    cadre=shapes.Drawing(19*cm,5*cm)

    text_regideso=shapes.String(0*mm,4.3*cm,'REGIDESO',fontName="Helvetica-Bold",fontSize=19,fillColor="#000000")
    cadre.add(text_regideso)
    text_s=shapes.String(0*mm,3.3*cm,'D.U KINSHASA NORD',fontName="Helvetica-Bold",fontSize=13,fillColor="#000000")
    cadre.add(text_s)
    text_s=shapes.String(0*mm,2.6*cm,'Secteur: ',fontName="Helvetica-Bold",fontSize=13,fillColor="#000000")
    cadre.add(text_s)
    text_s=shapes.String(0*mm,1.9*cm,'Code: ',fontName="Helvetica-Bold",fontSize=13,fillColor="#000000")
    cadre.add(text_s)

    text_s=shapes.String(4.5*cm,0.8*cm,'BORDEREAUX DES DECAISSEMENTS',fontName="Helvetica-Bold",fontSize=17,fillColor="#000000")
    cadre.add(text_s)
    
    text_s=shapes.String(7.5*cm,0*cm,'Journée de ............',fontName="Helvetica-Bold",fontSize=13,fillColor="#000000")
    cadre.add(text_s)
    '''ligne=shapes.Line(0*cm,0*cm, 15*cm,0.7*cm,strokeColor="#000000", strokeWidth=0*mm)
    cadre.add(ligne)'''

    elements.append(cadre)

    styleDetail = ParagraphStyle(
                name='xxxstyle',
                fontName='Helvetica',
                fontSize=14,
                leading=21,
                alignment=TA_LEFT
                )

    elements.append(Spacer(1, 10))


    Dinsert=[]
    entete1=['CODE','N° ACQUIT','N° ABONNE','PERIODE','N° FACTURE','MONTANT','ESCOMPTE']
    Dinsert.append(entete1)
    
    for x in range(1,17):
        ligne=['','','','','','','']
        Dinsert.append(ligne)

    lignetot=['','','','','','58000','']
    Dinsert.append(lignetot)
    
    
    table=Table(Dinsert, hAlign='LEFT',vAlign='TOP',colWidths=[1.8*cm,3.3*cm,3.3*cm,2*cm,3.3*cm,3.3*cm,3.3*cm])
    table.setStyle(TableStyle([
            ('LEFTPADDING', (0, 0), (-1, -1), 2*mm),
            ('RIGHTPADDING', (0, 0), (-1, -1), 2*mm),
            ('TOPPADDING', (0, 0), (-1, -1), 2*mm),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2*mm),
            ('TOPPADDING', (0, 0), (-1, 0), 4*mm),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 4*mm),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('TEXTCOLOR', (0, 0), (-1, -1), '#000000'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('GRID', (0, 0), (-1, -2), 0.5, '#000000'),
            ('GRID', (5, -1), (5, -1), 0.5, '#000000'),
            ('FONTNAME', (5, -1), (5, -1), 'Helvetica-Bold'),
            ('ALIGN', (5, 1), (5, -1), 'RIGHT'),
            
            
            ]))
    elements.append(table)



    elements.append(Spacer(1, 10))

    foot=Paragraph('''
                   NOM DU CAISSIER .................................   <br />
                   SIGNATURE ............................   <br />
                   NOM DU RESPONSABLE COMMERCIAL ...............................<br />
                   SIGNATURE
                   ''', style=styleDetail)
    elements.append(foot)

    doc = SimpleDocTemplate(buffer, pagesize=letter,leftMargin=0.5*cm,topMargin=0.5*cm,bottomMargin=0.5*cm )
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline;filename=bordereau_decaissement.pdf'
    return response