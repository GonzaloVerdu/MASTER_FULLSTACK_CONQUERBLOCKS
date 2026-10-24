
'''
from nltk.tokenize import sent_tokenize, word_tokenize, wordpunct_tokenize
texto = f'El ticket #421 llegó ayer. Ana no pudo entrar: la clave expliró a las 08:00. ¿Lo reabrimos?'

frases: list[str] = sent_tokenize(texto, language='spanish')
print(frases)

palabras: list[str] = word_tokenize(texto, language='spanish')
print(palabras)

tosco: list[str]= wordpunct_tokenize(texto)
print(tosco)

from nltk.tokenize import regexp_tokenize, TweetTokenizer

logs=f'error timeout user: ana tocket:#421 retry=3'

trozos = regexp_tokenize(logs, pattern=r"\w+")
print(trozos)

tt= TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
print(tt.tokenize("Oye @soporte el login noooo va #urgente https://x.app/login"))
'''

from newspaper import Article, Config, Source

config = Config() #Como en este tipo de funciones, primero construyo una variable que llame a la función y me simplifica el tema
config.browser_user_agent = ( #Eso no es un navegador. Media redacción lo filtra: te devuelven 403, una página de “enable JavaScript”, o HTML vacío. Tú lo ves como “no extrae el artículo”. No es que #download() esté mal; es que el periódico no te quiere dejar pasar.
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
"(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)
config.request_timeout=15
config.fetch_images=False
config.language=('es')
config.memoize_articles=False

url = "https://www.abc.es/opinion/juan-manuel-de-prada-caridad-loca-demagogo-20260904191133-nt.html"

articulo= Article(url, config=config)
articulo.download() #GET del HTML. Rellena article.html. Con esto accedo a la información
articulo.parse() #Esto me hace las particiones necesarias del código HTML. A partir de aqui puedo empezar a acceder al título, texto, fecha, etc
# articulo.build() sustituiría a .download + .parsed()

articulo.title
articulo.authors
articulo.text
articulo.publish_date

#intento crear el archivo, y si no me deja porque ya existe, sobreeescribe el txt con el título del archivo=titulo del artículo
try:
    with open(f'{articulo.title}.txt', 'x') as f:
        f.write(articulo.text)

except FileExistsError:
    with open(f'{articulo.title}.txt', 'w') as f:
            f.write(f"{articulo.title}\n{articulo.publish_date}\n\n{articulo.text}")

#ahora toca la digitalización

from gtts import gTTS
try:
    tts= gTTS(articulo.text, lang='es', tld='es', slow=False)
    tts.save(f'{articulo.title}.mp3')

except gTTSError:
    print('La red ha fallado, compruebe su conexión a internet.')

'''
#Esto sería para darle la vuelta a las portadas de los periódicos
url_abc='https://www.abc.es/'

portada=Source(url_abc, config=config)
portada.build()
portada.download()
portada.parse()


print(portada.size())
lista_urls = [a.url for a in portada.articles[:10]]

for url in lista_urls:
    print(url)
    url1= Article(url, config=config)
    url1.download()
    url1.parse()

    with open(f'{url1.title}.txt', 'w') as f:
                f.write(f"{url1.title}\n{url1.publish_date}\n\n{url1.text}")
'''

