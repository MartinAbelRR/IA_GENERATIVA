nombre = 'martin'
apellido = 'reyes'
edad = 23

print('Hola, mi nombre es', nombre, 'y tengo', edad, 'años')

if nombre == 'martin':
    print('Hola Martin')
elif nombre == 'reyes':
    print('Hola Reyes')
else:
    print('Hola desconocido')

# Juntar los nombres
palabra = ''
palabra += nombre
palabra += ' '
palabra += apellido

print('Hola', palabra)