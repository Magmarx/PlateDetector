intalaciones para deteccion de placas
    # tener el build de openalpr instalado
    # instalar python 3.6 
    # Correr el comando -> pip install arrow    

Scripts para probar los diferentes tipos de detecciones
    # python main.py --file filepath --opcion --noDel jsonData --report date time -> para poder generar un reporte
    # python main.py --file filepath --rest --noDel dataRest -> para poder generar una transacción que se enviara a M5
    # python main.py --file filepath --text --noDel -> para poder generar un log 
    # python main.py --file filepath --log --noDel -> para poder desplegar el log en la consola del proceso que sucede en tiempo real
    # python main.py --file filepath --log --noDel jsonData --report day/month/year time --dev channel -> a couple heads up is that the time is a int and it will be on a 24 hour schedule
    # python reportGenerator.py --folder --reportType  --dev/prod path 

Installation for the openpyxl - the library for generating excel reports
    # pip install openpyxl
    # when you want to use the file images like png, jpeg, bmp install the dependence -- pip install pillow
    # openpyxl documentation https://openpyxl.readthedocs.io/en/stable/
    # openpyxl tutorial https://openpyxl.readthedocs.io/en/stable/tutorial.html#create-a-workbook