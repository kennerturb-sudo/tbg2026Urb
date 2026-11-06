# Variant 1
'''
length = float(input('Sisesta oma pikkus (cm): '))
weight = float(input('Sisesta oma kaal (kg): '))

bmi = round(weight / (length / 100) ** 2, 1)
print('Sinu kehamassiindeks on ' + str(bmi))
if bmi < 18.5:
    print('Oled alakaalus.')
elif 18.5 <= bmi < 25:
    print('Sinu kehakaal on normaalne.')
elif 25 <= bmi < 30:
    print('Oled ülekaalus.')
else:
    print('Oled rasvunud.')
'''

# Variant 2
print('Sinu kehamassiindeks on ' +
      str(round(float(input('Sisesta oma kaal (kg): ')) /
                (float(input('Sisesta oma pikkus (cm): ')) / 100) ** 2, 1)))