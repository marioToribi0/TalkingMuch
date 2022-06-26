import string
import os
# 17 - 20 de junio. Mario Toribio 2021
# Restricciones:
# 1. Los nombres del usuario no pueden tener ":"

frasesProhibidas = ["You blocked this contact. Tap to unblock.", "You unblocked this contact.", "<Media omitted>",
                    "This message was deleted", "changed the group description", "You're now an admin", "You deleted this message"]
months = {1: "january", 2: "february", 3: "march", 4: "april", 5: "may", 6: "june",
          7: "july", 8: "august", 9: "september", 10: "october", 11: "november", 12: "december"}
# Frases mensajes borrados
frasesBorrar = ["You deleted this message", "This message was deleted"]


def remplazarEmojis(text, bool=False):
    cadena = ""
    letras = string.ascii_letters + "áéíóú" + " " + "ñÑ"
    if (bool):
        letras += "\n"
    for letter in text:
        if (letter not in letras):
            continue
        cadena += letter
    return cadena


def verificationDate(date):
    pos = date.find(",")
    dates = date[:pos]
    dates = dates.split("/")
    for i in dates:
        if not i.isnumeric():
            return False
    return (len(dates) == 3)


def encontrarUsuario(line):
    usuario = line[line.find("-")+1:line.find(":", line.find("-"))]
    return usuario.lstrip().rstrip()


def borrarPantalla():
    os.system("cls")

# Comprueba si una línea es un mensaje de whatsapp


def verificarLinea(line):
    if (line[line.find("-")+1:].lstrip().rstrip() in frasesProhibidas):
        return True
    if (len(line.split(":")) <= 2):
        return True
    return False


def obtenerMensaje(line):
    if (verificationDate(line) and not verificarLinea(line)):
        return line.split(":")[2].lstrip()
    else:
        return line


class Archivo():
    def __init__(self, ubicacion):
        self.file = open(ubicacion, encoding="utf8")
        # self.file = ubicacion
        self.words = dict()
        # Frecuencia de mensajes por período
        self.date = {"day": {}, "month": {}, "year": {}, "hour": {}}
        self.users = []                                                 # Usuarios
        # Palabras por usuario
        self.wordsPeople = {}
        self.dateStatus = False
        self.wordStatus = True
        self.initializeUsers()
        self.initializeWordsPeople()
        self.initializeWords()

    def initializeWordsPeople(self):
        for user in self.users:
            self.wordsPeople[user] = {}

    def messageDelete(self):
        self.file.seek(0)
        resultado = {}
        for line in self.file:
            if (obtenerMensaje(line.lstrip().rstrip()) in frasesBorrar):
                user = encontrarUsuario(line)
                resultado[user] = resultado.get(user, 0) + 1

        return sorted([(k, v) for (v, k) in resultado.items()], reverse=True)

    def initializeUsers(self):
        self.file.seek(0)
        for line in self.file:
            if (not verificationDate(line)):
                continue
            if (verificarLinea(line) == True):
                continue
            user = encontrarUsuario(line)
            if (user not in self.users):
                self.users.append(user)

    # Si dirección es True, mayor a menor
    def returnTupleWordPeople(self, cantidad, letras=6, direccion=True):
        if (cantidad == None):
            return None
        # {user: {"word": count, "wordTwo": count}}
        # return {user: [(count, "word"), (count, "word")]}
        result = {}
        for user in self.wordsPeople.keys():
            lista = []
            # [(user, {"word": count, "wordTwo":count})]
            for word, count in self.wordsPeople[user].items():
                if (len(word) > letras):
                    lista.append((count, word))
            lista.sort(reverse=True)
            # Reducir a número de palabras
            listaReducida = []
            for i in range(cantidad):
                if i>=len(lista):
                    break
                listaReducida.append(lista[i])
            result[user] = listaReducida

        return result

    def mostTalked(self):
        diccionary = dict()
        for user in self.users:
            diccionary[user] = 0
        self.file.seek(0)
        lastLine = None
        for line in self.file:
            try:
                if (not verificationDate(line)):
                    text = line
                    if (lastLine != None):
                        usuario = encontrarUsuario(lastLine)
                    else:
                        continue
                else:
                    lastLine = line
                    text = line
                    pos = text.find(":", text.find(":")+1)
                    text = text[pos+1:]
                    usuario = encontrarUsuario(line)
                    if (verificarLinea(line) == True):
                        continue
            except:
                continue
            diccionary[usuario] += 1
        # Ordenar diccionario
        resultado = {}
        lista = []

        for key, value in diccionary.items():
            lista.append((value, key))
        lista.sort(reverse=True)

        for i in lista:
            resultado[i[1]] = i[0]

        return resultado

    def countWords(self):
        if (self.wordStatus == False):
            self.initializeWords()
            self.wordsStatus = True
        return self.words

    def countPhrases(self, phrase):
        if (phrase == None):
            return None
        diccionary = dict()
        for user in self.users:
            diccionary[user] = [phrase, 0]
        self.file.seek(0)
        lastLine = None
        for line in self.file:
            try:
                if (not verificationDate(line)):
                    text = line
                    if (lastLine != None):
                        usuario = encontrarUsuario(lastLine)
                    else:
                        continue
                else:
                    lastLine = line
                    text = line
                    pos = text.find(":", text.find(":")+1)
                    text = text[pos+1:]
                    usuario = encontrarUsuario(line)
                    if (verificarLinea(line) == True):
                        continue
            except:
                continue
            text = remplazarEmojis(text, True).lower()

            if (line[line.find(":", line.find(":")+1)+1:].lstrip().rstrip() in frasesProhibidas):
                continue
            count = 0
            countPhrase = text.count(phrase)
            posicion = text.find(phrase) + 1

            # Comprobar si es una frase exacta
            while (posicion != 0):
                if (countPhrase == 0):
                    break
                if ((text[posicion + len(phrase)-1] in [" ", "\n"]) and (text[posicion-2] == " ")):
                    count += 1
                posicion = text.find(phrase, posicion) + 1

            diccionary[usuario][1] += count

        resultado = {}
        lista = []

        for key, value in diccionary.items():
            lista.append((value, key))
        lista.sort(reverse=True)

        for i in lista:
            resultado[i[1]] = i[0]

        return resultado

    def frequencyPeriod(self, tuple=("day", 10), direccion=True):
        if (tuple == None):
            return None
        date = tuple[0]
        cant = tuple[1]
        if (date not in ["day", "month", "year", "hour"]):
            return None
        if (self.dateStatus == False):
            self.dateStatus = True
            self.initializeDate()
        dates = []
        result = []
        for key, value in self.date[date].items():
            dates.append((value, key))
        dates.sort(reverse=direccion)
        if (cant > len(self.date[date])):
            cant = len(self.date[date])
        for i in range(cant):
            value, key = dates[i]
            result.append((key, value))
        return result

#{dia: {}, mes:{}, año: {}}
    def initializeDate(self):
        self.file.seek(0)
        for date in self.file:
            try:
                if (not verificationDate(date)):
                    continue
            except:
                continue
            # Obtener hora y si es AM o PM
            # {"hour": {"01 AM"}
            hour = date.split(",")[1].split("-")[0].split(":")[0] + " " + \
                date.split(",")[1].split("-")[0].split(":")[1].split()[1]
            self.date["hour"][hour] = self.date.get("hour").get(hour, 0) + 1
            # Formatear fecha
            date = date.split(",")[0]
            # dias
            self.date["day"][date] = self.date.get("day").get(date, 0) + 1
            # mes
            pos = date.find("/")
            monthDate = date[:pos]
            self.date["month"][months[int(monthDate)]] = self.date.get(
                "month").get(months[int(monthDate)], 0) + 1
            # años
            yearDate = "20" + date.split("/")[2]

            self.date["year"][yearDate] = self.date.get(
                "year").get(yearDate, 0) + 1

    def initializeWords(self):
        self.file.seek(0)
        for line in self.file:
            # Almacenar el espacio donde se encuentra la línea como constante en el bucle
            lineConst = line
            # Línea para modificar
            line = line.rstrip()
            if (verificarLinea(line) == True):
                continue
            if (line[line.find(":", line.find(":")+1)+1:].lstrip().rstrip() in frasesProhibidas):
                continue
            position = line.find(":", line.find(":") + 1)
            line = line[position + 1:]
            # Words
            line = line.lower()
            line = remplazarEmojis(line)
            line = line.split()

            UsuarioAnterior = None
            for word in line:
                # Agregar palabra al diccionario general
                self.words[word] = self.words.get(word, 0) + 1
                # Buscar usuario
                # Se comprueba que la línea funciona
                try:
                    if (verificationDate(lineConst) == True):
                        user = encontrarUsuario(lineConst)
                        UsuarioAnterior = user
                except:
                    pass
                # Agregar palabras al diccionario de usuarios
                self.wordsPeople[user][word] = self.wordsPeople.get(
                    user).get(word, 0) + 1

    def bestWords(self, cantidad, letters=10):
        if (cantidad == None) or (type(cantidad) == tuple):
            return None
        if (self.wordStatus == False):
            self.initializeWords()
            self.wordsStatus = True
        words = []
        result = []
        for key, value in self.words.items():
            words.append((value, key))
        words.sort(reverse=True)

        if (cantidad > len(self.words)):
            cantidad = len(self.words)

        count = 0
        i = 0
        while(count < cantidad):
            value, key = words[i]
            if (len(key) > letters):
                result.append((key, value))
                count += 1
            i += 1
            if (i >= len(words)):
                break
        return result
    
    def generateFile(self, nameFile):
        resultFile = nameFile
        lista = self.bestWords(50)
        for key, value in lista:
            if value == 1:
                resultFile.write(f"{key.capitalize()}: {value} message\n")
            else:
                resultFile.write(f"{key.capitalize()}: {value} messages\n")
        
        return resultFile

def menu():
    while(1):
        print("¿Qué deseas hacer?")
        print("\t1. Generar documento con conteo por palabras.")
        print("\t2. Palabras más utilizadas.")
        print("\t3. Mostrar frecuencia de mensajes por período.")
        print("\t4. Buscar una frase.")
        print("\t5. Mensajes por persona.")
        print("\t6. Palabras más comunes por persona.")
        print("\t7. Mensajes borrados por persona.")

        try:
            option = int(input("\nIngresa la opción: "))
            if (option in range(1, 8)):
                return option
            else:
                raise Exception
        except TypeError:
            print("Esa opción no es válida")
            input()
            borrarPantalla()
        except Exception:
            print("Esa opción no es válida")
            input()
            borrarPantalla()


def excepciones(value):
    if ((value == False) or (value == None)):
        return None
    if ((value == 2) or (value == 6)):
        while(1):
            try:
                n = int(input("Cantidad de palabras a presentar: "))
                letter = int(input("Cantidad de letras: "))
                return n
            except:
                print("No has escrito un número\n")
                input()
                borrarPantalla()
    elif (value == 3):
        while(1):
            opciones = {1: "day", 2: "month", 3: "year", 4: "hour"}
            try:
                borrarPantalla()
                print("\t1. Por días.")
                print("\t2. Por meses.")
                print("\t3. Por años.")
                print("\t4. Por horas")
                date = int(input("Opción: "))
                cant = int(input("Datos a mostrar: "))
                if (date not in range(1, 5)):
                    raise Exception("opciones")

                return opciones[date], cant

            except TypeError:
                print("Error al ingresar los datos\n")
                input()
                borrarPantalla()
            except Exception as inst:
                if (inst.args[0] == "opciones"):
                    print("Esa opción no está disponible\n")

    elif (value == 4):
        phrase = input("Escribe la frase a buscar: ")
        return phrase


def show(option, enter, objeto):
    borrarPantalla()
    if (option == 1):
        nameFile = "Documentos con Resultados.txt"
        resultFile = open(nameFile, "w")
        lista = objeto.bestWords(len(enter))
        for key, value in lista:
            if value == 1:
                resultFile.write(f"{key.capitalize()}: {value} mensaje\n")
            else:
                resultFile.write(f"{key.capitalize()}: {value} mensajes\n")
        print(f"Listo. El documento generado se llama: {nameFile}")
        resultFile.close()
    elif (option == 2):
        print(f"\n\t Top {len(enter)}")
        for key, value in enter:
            if (value != 1):
                print(f"{key.capitalize()} con {value} mensajes")
            else:
                print(f"{key.capitalize()} con {value} mensaje")
    elif (option == 3):
        print(f"\t Top {len(enter)}")
        for key, value in enter:
            if (value != 1):
                print(f"{key.capitalize()} con {value} mensajes")
            else:
                print(f"{key.capitalize()} con {value} mensaje")
    elif (option == 4):
        word = enter[objeto.users[0]][0]
        print(f"Para {word}:")
        for person in enter.keys():
            print(f"{person} con {enter[person][1]} \"{enter[person][0]}\"")
    elif (option == 5):
        print("\tCantidad de mensajes")
        for key, value in enter.items():
            print(f"{key} con {value} mensajes")
    elif (option == 6):
        # return {user: [(count, "word"), (count, "word")]}
        for user, palabras in enter.items():
            print(f"\tPara {user}:")
            for contador, palabra in palabras:
                print(f"\"{palabra}\" con {contador} veces")
            print()
    elif (option == 7):
        print("\tMensajes borrados:")
        for value, key in enter:
            if (value != 1):
                print(f"{key} con {value} mensajes")
            else:
                print(f"{key} con {value} mensaje")


def mainLoop(name):
    handle = Archivo(name)
    while (1):
        value = menu()
        def comprobation(value, comp): return False if (
            value != comp) else value
        options = {1: handle.words, 2: handle.bestWords(excepciones(comprobation(value, 2))),
                   3: handle.frequencyPeriod(excepciones(comprobation(value, 3))), 4: handle.countPhrases(excepciones(comprobation(value, 4))),
                   5: handle.mostTalked(), 6: handle.returnTupleWordPeople(excepciones(comprobation(value, 6))), 7: handle.messageDelete()}

        show(value, options[value], handle)
        input()
        print()
        borrarPantalla()


def main():
    handleName = input("Ingresa un archivo: ")
    #handleName = 'C:\\Users\\Mtr_y\\Desktop\\INTEC\\4TO TRIMESTRE\\JAVASCRIPT\\Curso\\Pagina 1\\tkinter\\freecodecamp\\grupo.txt'
    while(1):
        try:
            mainLoop(handleName)
            break
        except FileNotFoundError:
            print(f"El archivo no fue encontrado: {handleName}")
            handleName = input("Ingresa un archivo: ")
            #handleName = 'C:\\Users\\Mtr_y\\Desktop\\INTEC\\4TO TRIMESTRE\\JAVASCRIPT\\Curso\\Pagina 1\\tkinter\\freecodecamp\\carla.txt'


if __name__ == "__main__":
    main()
    input()
