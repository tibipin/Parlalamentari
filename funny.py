import requests
from bs4 import BeautifulSoup
import pandas

judete = ['Alba', 'Arad', 'Arges', 'Bacau', 'Bihor', 'Bistrita-Nasaud', 'Botosani', 'Brasov', 'Braila', 'Bucuresti'
          'Buzau', 'Caras-Severin', 'Calarasi', 'Cluj', 'Constanta', 'Covasna', 'Dambovita', 'Dolj', 'Galati',
          'Giurgiu', 'Gorj', 'Harghita', 'Hunedoara', 'Ialomita', 'Iasi', 'Ilfov', 'Maramures', 'Mehedinti', 'Mures',
          'Neamt', 'Olt', 'Prahova', 'Satu-Mare', 'Salaj', 'Sibiu', 'Suceava', 'Teleorman', 'Timisoara', 'Tulcea',
          'Valcea', 'Vaslui', 'Vrancea']

lista_candidati = []
camera_candidati = []
lista_intrebari = []
lista_raspunsuri = []
lista_rezultate = []
dictionar_final = dict()


for j in judete:
    if j != 'Bucuresti':
        url = f'https://recorder.ro/candidatii-judetului-{j}'
    else:
        url = 'https://recorder.ro/candidati-bucuresti/'
    t = requests.get(url=url)
    supa = BeautifulSoup(t.text, 'html.parser')

    # Lista de candidati per pagina
    lista_parlamentari = supa.find_all('h3', {'class': 'block-parlamentar-nume mt-0'})
    for candidat in lista_parlamentari:
        lista_candidati.append(candidat.text.strip('\n'))


    # Lista de camere
    camere = supa.find_all('span', {'class': 'block-parlamentar-attributes-camera'})
    for camera in camere:
        camera_candidati.append(camera.text.strip('\n'))

    # Rubrica de intrebari per candidat
    rubrica_intrebari = supa.find_all('div', {'class', 'row align-items-center'})
    for i in range(0, len(rubrica_intrebari), 5):
        focus_candidat = rubrica_intrebari[i:i+5]
        for element in focus_candidat:
            intrebare = element.contents[1].text.strip('\n')
            raspuns = element.contents[3].text.strip('\n')
            lista_intrebari.append(intrebare)
            lista_raspunsuri.append(raspuns)

    t.close()

for i in range(0, len(lista_intrebari), 5):
    intrebari = lista_intrebari[i:i+5]
    raspunsuri = lista_raspunsuri[i:i+5]
    rezultate = dict(zip(intrebari, raspunsuri))
    candidat = lista_candidati[i//5]
    camera = camera_candidati[i//5]
    dictionar_final.update({candidat: {'camera': camera, 'optiuni': rezultate}})

df = pandas.DataFrame()

for element in dictionar_final.keys():
    temp_df = pandas.DataFrame([dictionar_final[element]['optiuni']])
    temp_df.columns = ['Revenirea la alegerile locale în două tururi',
                       'Reducerea semnificativă a aparatului bugetar',
                       'Anularea imunității parlamentare în ceea ce privește justiția',
                       'Pierderea mandatului parlamentar în caz de traseism (în ipoteza revizuirii Constituției)',
                       'Introducerea educației sexuale în școli']
    temp_df['candidat'] = element
    temp_df['camera'] = dictionar_final[element]['camera']
    df = df.append(temp_df)

df.to_excel('lol.xlsx', index=False)